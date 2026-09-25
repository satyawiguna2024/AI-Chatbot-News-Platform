import asyncio

from app.db import AsyncSessionLocal
from app.services import (
    NewsAPIClient,
    ArticleContentChunker,
    ArticleContentCleaner,
    ArticleExtractor,
    ArticleService,
    ArticleTranslator,
    EmbeddingService,
)


BATCH_SIZE = 100
TOTAL_ARTICLES = 300


async def ingest_news():
  news_client = NewsAPIClient()

  article_service = ArticleService(
    extractor=ArticleExtractor(),
    translator=ArticleTranslator(),
    cleaner=ArticleContentCleaner(),
    chunker=ArticleContentChunker(),
    embedding=EmbeddingService(),
  )

  total_processed = 0

  # 300 artikel / 100 artikel per batch = 3 batch.
  total_pages = (TOTAL_ARTICLES + BATCH_SIZE - 1) // BATCH_SIZE

  for page in range(1, total_pages + 1):
    remaining = TOTAL_ARTICLES - total_processed

    # Batch terakhir bisa kurang dari 100.
    page_size = min(BATCH_SIZE, remaining)

    print()
    print("=" * 60)
    print(f"Fetching page {page}/{total_pages}")
    print(f"Requesting {page_size} articles")
    print("=" * 60)

    articles = await news_client.get_everything(
      page=page,
      page_size=page_size,
    )

    if not articles:
      print("No more articles returned by NewsAPI.")
      break

    print(f"Received {len(articles)} articles.")

    for index, news_article in enumerate(articles, start=1):
      print("-" * 60)
      print(
        f"Processing article "
        f"{index}/{len(articles)} "
        f"(total: {total_processed + 1}/{TOTAL_ARTICLES})"
      )
      print(f"Title: {news_article.title}")
      print(f"URL: {news_article.url}")

      try:
        async with AsyncSessionLocal() as session:
          article = await article_service.ingest_article(
            session=session,
            news_article=news_article,
          )

        total_processed += 1

        print(f"Saved article ID: {article.id}")

      except Exception as exc:
        print(f"FAILED: {news_article.url}")
        print(f"Error: {exc}")
        continue # proses artikel berikutnya.

    print()
    print("=" * 60)
    print(f"Batch {page}/{total_pages} completed.")
    print(f"Total processed: {total_processed}/{TOTAL_ARTICLES}")
    print("=" * 60)

    if total_processed >= TOTAL_ARTICLES:
      break

  print()
  print("=" * 60)
  print("INGESTION FINISHED")
  print(f"Total processed: {total_processed}/{TOTAL_ARTICLES}")
  print("=" * 60)


if __name__ == "__main__":
  asyncio.run(ingest_news())