from uuid import UUID
from pydantic import BaseModel

from app.schemas.chat import ChatSource

class ConversationCreateRequest(BaseModel):
  anonymous_id: UUID
  article_id: int | None = None


class ConversationCreateResponse(BaseModel):
  conversation_id: UUID
  anonymous_id: UUID
  article_id: int | None

class ConversationContextRequest(BaseModel):
  anonymous_id: UUID

class ConversationMessageResponse(BaseModel):
  id: int
  role: str
  content: str
  sources: list[ChatSource] | None = None

class ConversationContextResponse(BaseModel):
  conversation_id: UUID | None
  anonymous_id: UUID
  article_id: int | None
  messages: list[ConversationMessageResponse]