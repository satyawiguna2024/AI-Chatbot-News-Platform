from openai import AsyncOpenAI
from app.core import get_settings


class RAGChatService:
  def __init__(self):
    settings = get_settings()
    self.client = AsyncOpenAI(base_url=settings.openrouter_base_url, api_key=settings.openrouter_api_key)
    self.model = "nex-agi/nex-n2.5-pro:free"

  async def generate_answer(
    self, *,
    question: str, context: str,
  ):
    if not question.strip():
      raise ValueError("Question cannot be empty.")

    if not context.strip():
      raise ValueError("Context cannot be empty.")

    response = await self.client.chat.completions.create(
      model=self.model,
      messages=[
        {
          "role": "system",
          "content": (
            "You are an AI assistant for an Indonesian news platform.\n\n"
            "Answer the user's question using only the provided context.\n"
            "Answer in the same language as the user's question.\n"
            "Do not invent information that is not supported by the context.\n"
            "If the context does not contain enough information, "
            "say that the information is not available in the provided article."
          ),
        },
        {
          "role": "user",
          "content": (
            f"Question:\n{question}\n\n"
            f"Context:\n{context}"
          ),
        },
      ],
    )

    message = response.choices[0].message

    if not message.content:
      raise ValueError("Chat model returned empty content.")

    return message.content