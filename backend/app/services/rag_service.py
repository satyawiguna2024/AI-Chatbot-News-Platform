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
    if not question.strip():
      raise ValueError("Question cannot be empty.")

    recent_messages = await self.conversation_service.get_recent_messages(
      session=session,
      conversation_id=conversation_id,
      limit=10,
    )

    # Dipanggil oleh chat service HANYA kalau LLM memutuskan butuh artikel.
    async def search_fn(query: str):
      print(f"RAG: TOOL search_articles query = {query!r}")

      query_embedding = await self.embedding_service.embed_text(query)

      results = await self.vector_search_service.search_similar_chunks(
        session=session,
        query_embedding=query_embedding,
        article_id=article_id,
        top_k=top_k,
      )

      print(f"RAG: RESULTS = {len(results)}")

      if not results:
        return "", []

      context = self.context_builder.build(results)

      # Di halaman detail artikel, kartu sumber tidak berguna
      # (user sudah berada di artikel itu), jadi tidak dikirim.
      sources = self.build_sources(results) if article_id is None else []

      return context, sources

    async for event in self.chat_service.stream_with_tools(
      question=question,
      messages=recent_messages,
      article_id=article_id,
      search_fn=search_fn,
    ):
      yield event

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