import pytest
from sqlalchemy import select

from app.db import AsyncSessionLocal
from app.models import ArticleChunk
# from app.schemas import NewsAPIArticle, NewsAPISource
from app.services import (
  ArticleService, ArticleExtractor,
  ArticleTranslator, ArticleContentCleaner,
  NewsAPIClient, ArticleContentChunker, EmbeddingService
)


@pytest.mark.asyncio
async def test_ingest_article():
  news_client = NewsAPIClient()

  # Ambil satu artikel dari NewsAPI.
  articles = await news_client.get_everything(
    # query="Indonesia",
    page_size=1,
  )

  assert len(articles) > 0

  # Service-service yang dibutuhkan ArticleService.
  article_service = ArticleService(
    extractor=ArticleExtractor(),
    translator=ArticleTranslator(),
    cleaner=ArticleContentCleaner(),
    chunker=ArticleContentChunker(),
    embedding=EmbeddingService()
  )

  async with AsyncSessionLocal() as session:
    article = await article_service.ingest_article(
      session=session,
      news_article=articles[0],
    )

    print("\n=== ARTICLE ===")
    print("ID:", article.id)
    print("TITLE:", article.title)

    # Ambil semua chunks milik artikel tersebut.
    result = await session.execute(
      select(ArticleChunk)
      .where(ArticleChunk.article_id == article.id)
      .order_by(ArticleChunk.chunk_index)
    )

    chunks = result.scalars().all()

    print("\n=== CHUNKS ===")
    for chunk in chunks:
      print(f"\nCHUNK {chunk.chunk_index}")
      print("Tokens:", chunk.token_count)
      print("Embedding dimension:", len(chunk.embedding))
      print("First 5 values:", chunk.embedding[:5])
      print(chunk.content)

    assert len(chunks) > 0
    assert all(
      chunk.embedding is not None
      for chunk in chunks
    )

    assert all(
      len(chunk.embedding) == 1536
      for chunk in chunks
    )