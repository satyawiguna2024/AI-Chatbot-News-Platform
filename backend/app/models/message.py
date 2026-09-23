from datetime import UTC, datetime
from uuid import UUID
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base

if TYPE_CHECKING:
  from app.models.conversation import Conversation


class Message(Base):
  __tablename__ = "messages"

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  conversation_id: Mapped[UUID] = mapped_column(PostgreSQLUUID(as_uuid=True), ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False, index=True)
  role: Mapped[str] = mapped_column(String(20), nullable=False)
  content: Mapped[str] = mapped_column(Text, nullable=False)
  sources: Mapped[list[dict] | None] = mapped_column(JSONB, nullable=True)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC))

  conversation: Mapped["Conversation"] = relationship(back_populates="messages")