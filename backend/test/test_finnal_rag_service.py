import pytest

from app.db import AsyncSessionLocal
from app.services import (
    EmbeddingService,
    VectorSearchService,
    RAGContextBuilder,
    RAGChatService,
    RAGService,
)


@pytest.mark.asyncio
async def test_rag_service():
  embedding_service = EmbeddingService()
  vector_search_service = VectorSearchService()
  context_builder = RAGContextBuilder()
  chat_service = RAGChatService()

  rag_service = RAGService(
    embedding_service=embedding_service,
    vector_search_service=vector_search_service,
    context_builder=context_builder,
    chat_service=chat_service,
  )

  question = "Berapa target jumlah desa nelayan yang akan dibangun pemerintah?"

  async with AsyncSessionLocal() as session:
    answer = await rag_service.ask(
      session=session,
      question=question,
      article_id=3,
      limit=5,
    )

  print("\n=== RAG SERVICE ANSWER ===")
  print(answer)

  assert answer