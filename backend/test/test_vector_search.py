import pytest

from app.db import AsyncSessionLocal
from app.services import EmbeddingService, VectorSearchService


@pytest.mark.asyncio
async def test_vector_search():
  embedding_service = EmbeddingService()
  vector_search = VectorSearchService()

  question = "Berapa target jumlah desa nelayan yang akan dibangun pemerintah?"

  query_embedding = await embedding_service.embed_text(question)
  async with AsyncSessionLocal() as session:
    results = await vector_search.search_similar_chunks(
      session=session,
      query_embedding=query_embedding,
      article_id=3,
      limit=3,
    )

  print("\n=== VECTOR SEARCH ===")
  print("Question:", question)

  for chunk, distance in results:
    print("\nCHUNK:", chunk.chunk_index)
    print("Distance:", distance)
    print("Content:", chunk.content[:500])

  assert len(results) > 0