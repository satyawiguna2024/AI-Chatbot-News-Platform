from datetime import datetime
from pydantic import BaseModel, ConfigDict


class NewsAPISource(BaseModel):
  id: str | None = None
  name: str


class NewsAPIArticle(BaseModel):
  source: NewsAPISource
  author: str | None = None
  title: str
  description: str | None = None
  url: str
  urlToImage: str | None = None
  publishedAt: datetime | None = None
  content: str | None = None
  model_config = ConfigDict(extra="ignore")