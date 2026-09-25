import pytest
from sqlalchemy import select

from app.db import AsyncSessionLocal
from app.models import ArticleChunk
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
    for news_article in articles:
      article = await article_service.ingest_article(
        session=session,
        news_article=news_article,
      )

      print("\n\n\n==============================")
      print("ARTICLE ID:", article.id)
      print("TITLE:", article.title)
      print("URL:", article.url)
      print("CONTENT:", article.content)
      print("CONTENT LENGTH:", len(article.content))
      print("TRANSLATED CONTENT LENGTH:", len(article.translated_content))

      result = await session.execute(
        select(ArticleChunk)
        .where(ArticleChunk.article_id == article.id)
        .order_by(ArticleChunk.chunk_index)
      )

      chunks = result.scalars().all()
      print("CHUNKS:", len(chunks))
      
      assert len(chunks) > 0

      assert all(
        chunk.embedding is not None
        for chunk in chunks
      )

      assert all(
        len(chunk.embedding) == 1536
        for chunk in chunks
      )
    
    