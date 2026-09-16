import httpx

from app.core import get_settings
from app.schemas import NewsAPIArticle


class NewsAPIClient:
  BASE_URL = "https://newsapi.org/v2"

  # initial
  def __init__(self):
    settings = get_settings()
    self.api_key = settings.news_api_key

  # method get_everything
  async def get_everything(
    self, *, query: str | None = None,
    page_size: int = 10, page: int = 1,
  ):
    params = {
      "pageSize": page_size,
      "page": page, "sortBy": "publishedAt",
      "language": "en", "domains": "detik.com,kompas.com,tribunnews.com,cnnindonesia.com,liputan6.com,tempo.co,republika.co.id,merdeka.com,okezone.com,sindonews.com,kumparan.com,suara.com,viva.co.id,inews.id,antaranews.com,jawapos.com,pikiran-rakyat.com,thejakartapost.com"
    }

    if query:
      params["q"] = query
      
    headers = {"X-Api-Key": self.api_key,}

    async with httpx.AsyncClient(base_url=self.BASE_URL, timeout=10.0) as client:
      response = await client.get(
        "/everything",
        params=params,
        headers=headers,
      )

    # print("\n=== NEWS API REQUEST ===")
    # print(f"Params: {params}")
    # print(f"URL: {response.url}")
    
    response.raise_for_status()
    data = response.json()
    # print("\n=== NEWS API DATA OBJECT ===")
    # print("DATA: ", data)
    
    return [
      NewsAPIArticle.model_validate(article)
      for article in data["articles"]
    ]