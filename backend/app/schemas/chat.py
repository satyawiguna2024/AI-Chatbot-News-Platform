from uuid import UUID
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
  anonymous_id: UUID
  article_id: int | None = Field(default=None)
  question: str = Field(min_length=1)


class ChatSource(BaseModel):
  article_id: int
  title: str
  source_name: str | None
  image_url: str
  url: str


class ChatResponse(BaseModel):
  conversation_id: UUID
  question: str
  answer: str
  sources: list[ChatSource]