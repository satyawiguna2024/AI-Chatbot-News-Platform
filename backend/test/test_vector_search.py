import pytest

from app.db import AsyncSessionLocal
from app.services import EmbeddingService, VectorSearchService


@pytest.mark.asyncio
async def test_vector_search():
  embedding_service = EmbeddingService()
  vector_search = VectorSearchService()

  questions = [
    "Apa itu BUK Migas?",
    "Kepada siapa BUK Migas akan melapor langsung?", 
    "Apa tujuan penguatan BUK Migas?", 
    "Masalah apa yang harus dihindari dalam perizinan lintas sektor?", 
    "Kerjasama seperti apa yang akan dilakukan BUK Migas dengan perusahaan swasta?",
  ]

  # article_id = 3
  
  for q in questions:
    query_embedding = await embedding_service.embed_text(q)
    
    print("\n=== QUERY EMBEDDING ===")
    print(f"Dimension: {len(query_embedding)}")
    print(f"First 10 values: {query_embedding[:10]}")
    
    print("\n=== VECTOR SEARCH ===")
    print(f"Question: \n{q}")

    async with AsyncSessionLocal() as session:
      results = await vector_search.search_similar_chunks(
        session=session,
        query_embedding=query_embedding
        # article_id=article_id
      )

    for chunk, distance in results:
      print("\nCHUNK:", chunk.chunk_index)
      print("Distance:", distance)
      print("Content Length:", len(chunk.content))
      print("Content:", chunk.content)

    assert len(results) <= 3
    # assert all(
    #   chunk.article_id == article_id
    #   for chunk, _ in results
    # )