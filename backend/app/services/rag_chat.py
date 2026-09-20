from openai import AsyncOpenAI
from app.core import get_settings
from app.models import Message


class RAGChatService:
  def __init__(self):
    settings = get_settings()
    self.client = AsyncOpenAI(base_url=settings.openrouter_base_url, api_key=settings.openrouter_api_key)
    self.model = "nex-agi/nex-n2.5-pro:free"

  async def generate_answer(
    self, *,
    question: str, context: str,
    messages: list[Message] | None = None
  ):
    if not question.strip():
      raise ValueError("Question cannot be empty.")

    if not context.strip():
      raise ValueError("Context cannot be empty.")

    conversation_messages = [
      {
        "role": "system",
        "content": (
          "You are an AI assistant for an Indonesian news platform.\n\n"
          "Answer the user's question using only the provided context.\n"
          "Use the conversation history only to understand references "
          "such as 'dia', 'itu', 'yang tadi', or follow-up questions.\n"
          "Do not use conversation history as factual evidence.\n"
          "The provided article context is the source of truth.\n"
          "Answer in the same language as the user's question.\n"
          "Do not invent information that is not supported by the context.\n"
          "If the context does not contain enough information, "
          "say that the information is not available in the provided article."
        ),
      },
    ]

    if messages:
      for message in messages:
        conversation_messages.append(
          {
            "role": message.role,
            "content": message.content,
          }
        )

    conversation_messages.append(
      {
        "role": "user",
        "content": (
          f"Context:\n{context}\n\n"
          f"Question:\n{question}"
        ),
      }
    )
    
    response = await self.client.chat.completions.create(
      model=self.model,
      messages=conversation_messages,
    )

    message = response.choices[0].message

    if not message.content:
      raise ValueError("Chat model returned empty content.")

    return message.content