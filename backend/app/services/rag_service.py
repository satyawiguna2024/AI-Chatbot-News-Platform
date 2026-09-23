from typing import Any
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Article, ArticleChunk
from app.services.embedding import EmbeddingService
from app.services.vector_search import VectorSearchService
from app.services.context_builder import RAGContextBuilder
from app.services.rag_chat import RAGChatService
from app.services.conversation import ConversationService


class RAGResult:
  def __init__(
    self, *,
    answer: str,
    sources: list[tuple[ArticleChunk, Article, float]],
  ):
    self.answer = answer
    self.sources = sources


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
      return RAGResult(
        answer="Relevant information was not found.",
        sources=[]
      )

    context = self.context_builder.build(results)
    if not context:
      return RAGResult(
        answer="Relevant information was not found.",
        sources=[]
      )

    answer = await self.chat_service.generate_answer(
      question=question,
      context=context,
      messages=recent_messages
    )
    
    return RAGResult(
      answer=answer,
      sources=results
    )

  async def stream(
    self, *,
    session: AsyncSession,
    question: str,
    conversation_id: UUID,
    article_id: int | None = None,
    top_k: int = 3,
  ):
    print("RAG: START")
    
    if not question.strip():
      raise ValueError("Question cannot be empty.")

    print("RAG: GET RECENT MESSAGES")
    
    recent_messages = await self.conversation_service.get_recent_messages(
      session=session,
      conversation_id=conversation_id,
      limit=10,
    )
    
    print(f"RAG: RECENT MESSAGES = {len(recent_messages)}")

    print("RAG: CREATE QUERY EMBEDDING")

    query_embedding = await self.embedding_service.embed_text(question)

    print("RAG: EMBEDDING CREATED")

    print("RAG: VECTOR SEARCH")
    
    results = await self.vector_search_service.search_similar_chunks(
      session=session,
      query_embedding=query_embedding,
      article_id=article_id,
      top_k=top_k,
    )
    
    print(f"RAG: VECTOR RESULTS = {len(results)}")
    
    sources = self.build_sources(results)
    
    print(f"RAG: SOURCES = {len(sources)}")

    context = self.context_builder.build(results)

    print(f"RAG: CONTEXT LENGTH = {len(context)}")

    print("RAG: CALL CHAT SERVICE")
    
    async for content in self.chat_service.stream_answer(
      question=question,
      context=context,
      messages=recent_messages,
    ):
      print(f"RAG: RECEIVED CHUNK = {content!r}")

      yield {"type": "token", "content": content}

    print("RAG: CHAT SERVICE FINISHED")
    yield {"type": "sources", "sources": sources}
    yield {"type": "done"}

  def build_sources(
    self,
    results: list[tuple[ArticleChunk, Article, float]]
  ):
    sources: list[dict] = []
    seen_article_ids: set[int] = set()

    for chunk, article, distance in results:
      if article.id in seen_article_ids:
        continue

      seen_article_ids.add(article.id)

      sources.append(
        {
          "article_id": article.id,
          "title": article.title,
          "source_name": article.source_name,
          "image_url": article.image_url,
          "url": article.url,
        }
      )

    return sources

