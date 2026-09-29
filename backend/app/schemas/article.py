from datetime import datetime
from pydantic import BaseModel


class ArticleListItem(BaseModel):
  id: int
  title: str
  translated_title: str | None
  description: str | None
  translated_description: str | None
  source_name: str | None
  author: str | None
  published_at: datetime | None
  image_url: str | None
  url: str


class ArticleListResponse(BaseModel):
  items: list[ArticleListItem]
  page: int
  limit: int
  total: int
  total_pages: int
  has_next: bool


class ArticleDetailResponse(BaseModel):
  id: int
  title: str
  description: str | None
  content: str | None

  translated_title: str | None
  translated_description: str | None
  translated_content: str | None
  translated_language: str | None

  source_name: str | None
  author: str | None
  published_at: datetime | None
  image_url: str | None
  url: str
  created_at: datetime