from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.embedding import EmbeddingService
from app.services.vector_search import VectorSearchService
from app.services.context_builder import RAGContextBuilder
from app.services.rag_chat import RAGChatService
from app.services.conversation import ConversationService


class RAGService:
  def __init__(
    self, *,
    embedding_service: EmbeddingService,
    vector_search_service: VectorSearchService,
    context_builder: RAGContextBuilder,
    chat_service: RAGChatService,
    conversation_service: ConversationService
  ):
    self.embedding_service = embedding_service
    self.vector_search_service = vector_search_service
    self.context_builder = context_builder
    self.chat_service = chat_service
    self.conversation_service = conversation_service

  async def ask(
    self, *,
    session: AsyncSession,
    question: str,
    conversation_id: UUID,
    article_id: int | None = None,
    top_k: int = 3
  ):
    if not question.strip():
      raise ValueError("Question cannot be empty.")
    
    recent_messages = await self.conversation_service.get_recent_messages(
      session=session,
      conversation_id=conversation_id,
      limit=10
    )

    query_embedding = await self.embedding_service.embed_text(question)
    results = await self.vector_search_service.search_similar_chunks(
      session=session,
      query_embedding=query_embedding,
      article_id=article_id,
      top_k=top_k
    )

    if not results:
      return "Relevant information was not found."

    context = self.context_builder.build(results)
    if not context:
      return "Relevant information was not found."

    return await self.chat_service.generate_answer(
      question=question,
      context=context,
      messages=recent_messages
    )

