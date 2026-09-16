import pytest
from app.services import EmbeddingService


@pytest.mark.asyncio
async def test_embed_text():
  embedding_service = EmbeddingService()

  embedding = await embedding_service.embed_text(
    "Indonesia memiliki banyak berita dan peristiwa penting."
  )

  print("\n\n\n=== EMBEDDING ===")
  print("Dimension:", len(embedding))
  print("First 10 values:", embedding[:10])

  assert len(embedding) == 1536
  assert all(isinstance(value, float) for value in embedding)

