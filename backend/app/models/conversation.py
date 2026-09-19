from datetime import UTC, datetime
from uuid import UUID, uuid4
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base

if TYPE_CHECKING:
  from app.models.message import Message


class Conversation(Base):
  __tablename__ = "conversations"

  id: Mapped[UUID] = mapped_column(PostgreSQLUUID(as_uuid=True), primary_key=True, default=uuid4)
  anonymous_id: Mapped[UUID] = mapped_column(PostgreSQLUUID(as_uuid=True), nullable=False, unique=True, index=True)
  article_id: Mapped[int | None] = mapped_column(ForeignKey("articles.id", ondelete="CASCADE"), nullable=True, index=True)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC))
  updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC))

  # Relationship
  messages: Mapped[list["Message"]] = relationship(back_populates="conversation", cascade="all, delete-orphan")