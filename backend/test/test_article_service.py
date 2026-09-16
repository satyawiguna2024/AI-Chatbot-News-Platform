import pytest
from sqlalchemy import select

from app.db import AsyncSessionLocal
from app.models import ArticleChunk
# from app.schemas import NewsAPIArticle, NewsAPISource
from app.services import (
  ArticleService, ArticleExtractor,
  ArticleTranslator, ArticleContentCleaner,
  NewsAPIClient, ArticleContentChunker
)


# @pytest.mark.asyncio
# async def test_ingest_article():
#   article_url = "https://en.antaranews.com/news/431145/brics-strength-must-bring-tangible-benefits-prabowo"

#   news_article = NewsAPIArticle(
#     source=NewsAPISource(
#       id=None,
#       name="ANTARA",
#     ),
#     author="Antaranews Com; Fathur Rochman; Raka Adji",
#     title="BRICS strength must bring tangible benefits: Prabowo",
#     description="President Prabowo Subianto emphasized that the collective strength of BRICS countries must be translated into tangible benefits for the public and strengthen ...",
#     url=article_url,
#     urlToImage=None,
#     publishedAt="2026-09-12 16:31:49+00:00",
#     content=None
#   )

#   extractor = ArticleExtractor()
#   translator = ArticleTranslator()
#   cleaner = ArticleContentCleaner()
#   service = ArticleService(
#     extractor=extractor,
#     translator=translator,
#     cleaner=cleaner
#   )

#   async with AsyncSessionLocal() as session:
#     article = await service.ingest_article(
#       session=session,
#       news_article=news_article,
#     )

#     print("\n\n=== DATABASE ARTICLE ===")
#     print("ID:", article.id)
#     print("TITLE:", article.title)
#     print("DESCRIPTION:", article.description)
#     print("CONTENT:", article.content[:500])
#     print("TRANSLATED TITLE:", article.translated_title)
#     print("TRANSLATED DESCRIPTION:", article.translated_description)
#     print("TRANSLATED CONTENT:", article.translated_content[:500])

#     assert article.id is not None
#     assert article.title
#     assert article.description
#     assert article.content
#     assert article.translated_title
#     assert article.translated_description
#     assert article.translated_content
#     assert article.translated_language == "id"

#     result = await session.execute(
#       select(Article).where(
#         Article.id == article.id
#       )
#     )

#     saved_article = result.scalar_one()

#     assert saved_article.id == article.id
#     assert saved_article.url == article_url
#     assert saved_article.content
#     assert saved_article.translated_content



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
      print(f"Tokens: {chunk.token_count}")
      print(chunk.content)

    assert len(chunks) > 0
    assert chunks[0].article_id == article.id