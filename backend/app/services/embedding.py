from openai import AsyncOpenAI
from app.core import get_settings


class EmbeddingService:
  def __init__(self):
    settings = get_settings()
    self.client = AsyncOpenAI(api_key=settings.openai_api_key)
    self.model = "text-embedding-3-small"

  async def embed_text(self, text: str):
    if not text.strip():
      raise ValueError("Text cannot be empty.")

    response = await self.client.embeddings.create(
      model=self.model,
      input=text
    )
    
    # print("\n\n\nDEBUG RESPONSE - embeddings -> ", response)

    return response.data[0].embedding