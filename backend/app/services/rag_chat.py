import json
from openai import AsyncOpenAI
from app.core import get_settings
from app.models import Message


SEARCH_TOOL = {
  "type": "function",
  "function": {
    "name": "search_articles",
    "description": (
      "Search the news article database. Call this ONLY when the user asks for "
      "articles, news, recommendations, or a question that needs facts from "
      "articles (including questions about the article they are reading). "
      "Do NOT call it for greetings, thanks, small talk, or general-knowledge "
      "questions that do not need news articles."
    ),
    "parameters": {
      "type": "object",
      "properties": {
        "query": {
          "type": "string",
          "description": "A concise search query summarizing what the user wants.",
        }
      },
      "required": ["query"],
    },
  },
}

TOOL_SYSTEM_PROMPT = """
You are an AI assistant for an Indonesian news platform.

TOOL USE:
- Use the search_articles tool when the user needs information from news articles
  (asking for articles, recommendations, news, or details of an article).
- For greetings, thanks, small talk, or simple general-knowledge questions,
  answer directly WITHOUT calling the tool.
- When you decide to use the tool, call it directly without writing any preamble.

ANSWERING:
- If tool results are relevant, use them as the primary source and do not invent
  details that are not in them.
- If the tool returns nothing relevant, say so briefly, then answer with general
  knowledge if appropriate. Never pretend general knowledge came from articles.
- Do not fabricate facts. State clearly when you are uncertain.
- For time-sensitive information, do not claim certainty unless the results support it.

LANGUAGE:
- Answer in the same language as the user's question.
- Keep simple questions simple and concise.
""".strip()


class RAGChatService:
  def __init__(self):
    settings = get_settings()
    self.client = AsyncOpenAI(
      base_url=settings.openrouter_base_url,
      api_key=settings.openrouter_api_key,
    )
    self.model = "cohere/north-mini-code:free"

  # ------------------------------------------------------------------
  # Cara lama (tanpa tool calling). Tetap dipertahankan untuk RAGService.ask()
  # ------------------------------------------------------------------
  def _build_messages(
    self, *,
    question: str,
    context: str,
    messages: list[Message],
  ):
    if not question.strip():
      raise ValueError("Question cannot be empty.")

    system_prompt = """
    You are an AI assistant for an Indonesian news platform.

    You can answer questions using two sources:

    1. Relevant news article context provided by the system.
    2. Your general knowledge.

    Follow these rules carefully:

    ARTICLE CONTEXT:
    - If the provided article context is relevant to the user's question,
      use it as the primary source of information.
    - Do not invent details that are not supported by the relevant article context.
    - When answering about the article, stay grounded in the provided context.

    GENERAL KNOWLEDGE:
    - If the article context is empty or not relevant to the user's question,
      you may answer using your general knowledge.
    - Do not pretend that general knowledge came from the provided articles.
    - If the question is a simple general-knowledge question, answer it directly
      instead of forcing it to relate to the article.
    - If there is no relevant information in the articles, briefly acknowledge this
      when useful, then answer using general knowledge.

    UNCERTAINTY:
    - Do not fabricate facts.
    - If you are uncertain about an answer, clearly state that you are uncertain.
    - For time-sensitive information such as current officials, current events,
      prices, or "today/latest" information, do not claim certainty unless the
      available information supports it.

    LANGUAGE:
    - Answer in the same language as the user's question.
    - Keep simple questions simple and concise.
    """

    chat_messages = [
      {
        "role": "system",
        "content": system_prompt.strip(),
      }
    ]

    for message in messages or []:
      chat_messages.append(
        {
          "role": message.role,
          "content": message.content,
        }
      )

    user_content = f"""
    User question:
    {question}

    Available article context:
    {context if context else "(No relevant article context was found.)"}
    """.strip()

    chat_messages.append(
      {
        "role": "user",
        "content": user_content,
      }
    )

    return chat_messages

  async def generate_answer(
    self, *,
    question: str,
    context: str,
    messages: list[Message] | None = None,
  ):
    chat_messages = self._build_messages(
      question=question,
      context=context,
      messages=messages,
    )

    response = await self.client.chat.completions.create(
      model=self.model,
      messages=chat_messages,
      max_tokens=300,
    )

    answer = response.choices[0].message.content
    if not answer or not answer.strip():
      raise ValueError("LLM returned an empty answer.")

    return answer.strip()

  async def stream_answer(
    self, *,
    question: str,
    context: str,
    messages: list[Message] | None = None,
  ):
    chat_messages = self._build_messages(
      question=question,
      context=context,
      messages=messages,
    )

    stream = await self.client.chat.completions.create(
      model=self.model,
      messages=chat_messages,
      max_tokens=300,
      stream=True,
    )

    async for chunk in stream:
      if not chunk.choices:
        continue

      content = chunk.choices[0].delta.content
      if content:
        yield content

  # ------------------------------------------------------------------
  # Cara baru: tool calling
  # ------------------------------------------------------------------
  def _build_tool_messages(
    self, *,
    question: str,
    messages: list[Message],
    article_id: int | None,
  ):
    system = TOOL_SYSTEM_PROMPT

    if article_id is not None:
      system += (
        "\n\nSCOPE: The user is currently reading one specific article. "
        "For questions about it (summary, details, etc.), call search_articles; "
        "the search is automatically limited to that article."
      )

    chat_messages = [{"role": "system", "content": system}]

    for message in messages or []:
      chat_messages.append({"role": message.role, "content": message.content})

    # chat.py sudah menyimpan pertanyaan user sebelum stream() dipanggil,
    # jadi biasanya sudah ada di history. Tambahkan hanya kalau belum ada.
    last = messages[-1] if messages else None
    if not last or last.role != "user" or last.content != question:
      chat_messages.append({"role": "user", "content": question})

    return chat_messages

  async def stream_with_tools(
    self, *,
    question: str,
    messages: list[Message],
    article_id: int | None,
    search_fn,  # async (query: str) -> tuple[str, list[dict]]  = (context, sources)
  ):
    chat_messages = self._build_tool_messages(
      question=question,
      messages=messages,
      article_id=article_id,
    )

    # ---- Putaran 1: LLM memutuskan perlu tool atau tidak ----
    tool_calls: dict[int, dict] = {}

    stream = await self.client.chat.completions.create(
      model=self.model,
      messages=chat_messages,
      tools=[SEARCH_TOOL],
      max_tokens=300,
      stream=True,
    )

    async for chunk in stream:
      if not chunk.choices:
        continue

      delta = chunk.choices[0].delta

      if delta.content:
        yield {"type": "token", "content": delta.content}

      # argumen tool call datang bertahap, gabungkan per index
      for tc in delta.tool_calls or []:
        slot = tool_calls.setdefault(tc.index, {"id": "", "name": "", "args": ""})
        if tc.id:
          slot["id"] = tc.id
        if tc.function and tc.function.name:
          slot["name"] = tc.function.name
        if tc.function and tc.function.arguments:
          slot["args"] += tc.function.arguments

    # Tidak ada tool call -> jawaban sudah selesai, TIDAK ada sources
    if not tool_calls:
      return

    # ---- Jalankan tool ----
    for index, slot in tool_calls.items():
      if not slot["id"]:
        slot["id"] = f"call_{index}"

    chat_messages.append({
      "role": "assistant",
      "content": None,
      "tool_calls": [
        {
          "id": slot["id"],
          "type": "function",
          "function": {
            "name": slot["name"],
            "arguments": slot["args"] or "{}",
          },
        }
        for slot in tool_calls.values()
      ],
    })

    sources: list[dict] = []
    seen: set[int] = set()

    for slot in tool_calls.values():
      try:
        args = json.loads(slot["args"] or "{}")
      except json.JSONDecodeError:
        args = {}

      query = (args.get("query") or question).strip()
      context, found = await search_fn(query)

      for source in found:
        if source["article_id"] not in seen:
          seen.add(source["article_id"])
          sources.append(source)

      chat_messages.append({
        "role": "tool",
        "tool_call_id": slot["id"],
        "content": context or "No relevant articles were found.",
      })

    # ---- Putaran 2: jawaban final dari hasil tool (tanpa tools lagi) ----
    final = await self.client.chat.completions.create(
      model=self.model,
      messages=chat_messages,
      max_tokens=500,
      stream=True,
    )

    async for chunk in final:
      if not chunk.choices:
        continue

      content = chunk.choices[0].delta.content
      if content:
        yield {"type": "token", "content": content}

    if sources:
      yield {"type": "sources", "sources": sources}