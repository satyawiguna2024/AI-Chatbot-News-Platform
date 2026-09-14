import pytest
from app.services import NewsAPIClient, normalize_article


@pytest.mark.asyncio
async def test_get_news():
  client = NewsAPIClient()

  articles = await client.get_everything(
      # query="Presiden Indonesia",
      page_size=10,
  )
  
  print("\n=== NEWS API RESULT ===")
  print(f"\nLength Data Article : {len(articles)} \n\n")
  for article in articles:
    print(f"Title                 : {article.title}")
    print(f"Source                : {article.source.name}")
    print(f"Author                : {article.author}")
    print(f"Published             : {article.publishedAt}")
    print(f"URL                   : {article.url}")
    print(f"Description           : {article.description}")
    print(f"Main Content Article  : {article.content}")
    print("-" * 80)

  # ASSERT -> PENGECEKAN
  # jika tidak memenuhi suatu kondisi -> statusnya akan Failed
  assert len(articles) > 0
  article = normalize_article(articles[0])
  
  assert article.title
  assert article.url
  assert article.source_name