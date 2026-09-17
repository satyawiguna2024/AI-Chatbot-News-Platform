from sqlalchemy.ext.asyncio import AsyncSession

from app.services.embedding import EmbeddingService
from app.services.vector_search import VectorSearchService
from app.services.context_builder import RAGContextBuilder
from app.services.rag_chat import RAGChatService


class RAGService:
  def __init__(
    self, *,
    embedding_service: EmbeddingService,
    vector_search_service: VectorSearchService,
    context_builder: RAGContextBuilder,
    chat_service: RAGChatService,
  ):
    self.embedding_service = embedding_service
    self.vector_search_service = vector_search_service
    self.context_builder = context_builder
    self.chat_service = chat_service

  async def ask(
    self, *,
    session: AsyncSession,
    question: str,
    article_id: int | None = None,
    limit: int = 5,
  ):
    if not question.strip():
      raise ValueError("Question cannot be empty.")

    query_embedding = await self.embedding_service.embed_text(question)
    results = await self.vector_search_service.search_similar_chunks(
      session=session,
      query_embedding=query_embedding,
      article_id=article_id,
      limit=limit,
    )

    if not results:
      return "Relevant information was not found."

    context = self.context_builder.build(results)
    if not context:
      return "Relevant information was not found."

    return await self.chat_service.generate_answer(
      question=question,
      context=context,
    )