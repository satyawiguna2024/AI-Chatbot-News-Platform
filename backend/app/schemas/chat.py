from uuid import UUID
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
  anonymous_id: UUID
  article_id: int | None = Field(default=None)
  question: str = Field(min_length=1)


class ChatResponse(BaseModel):
  conversation_id: UUID
  answer: str