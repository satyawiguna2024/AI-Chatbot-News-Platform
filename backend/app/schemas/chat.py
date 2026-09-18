from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
  question: str = Field(min_length=1)
  article_id: int | None = Field(default=None)


class ChatResponse(BaseModel):
  answer: str