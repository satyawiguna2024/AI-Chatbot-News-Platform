from openai import AsyncOpenAI
from app.core import get_settings
from app.models import Message


class RAGChatService:
  def __init__(self):
    settings = get_settings()
    self.client = AsyncOpenAI(base_url=settings.openrouter_base_url, api_key=settings.openrouter_api_key)
    self.model = "cohere/north-mini-code:free"

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

    for message in messages:
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
    messages: list[Message] | None = None
  ):
    print("CHAT: START")
    
    chat_messages = self._build_messages(
      question=question,
      context=context,
      messages=messages
    )
    
    print(f"CHAT: MESSAGES = {len(chat_messages)}")
    print("CHAT: CALL OPENROUTER")

    stream = await self.client.chat.completions.create(
      model=self.model,
      messages=chat_messages,
      max_tokens=300,
      stream=True
    )
    
    print("CHAT: STREAM CREATED")

    async for chunk in stream:
      print(f"CHAT: RAW CHUNK = {chunk}")
      
      if not chunk.choices:
        continue

      content = chunk.choices[0].delta.content
      
      print(f"CHAT: CONTENT = {content!r}")
      if content:
        yield content
        
    print("CHAT: STREAM FINISHED")
