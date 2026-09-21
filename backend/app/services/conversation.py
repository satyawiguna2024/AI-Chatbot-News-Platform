from datetime import UTC, datetime, timedelta
from uuid import UUID
import logging
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Conversation, Message

logger = logging.getLogger(__name__)

class ConversationService:
  async def get_active_conversation(
    self, *,
    session: AsyncSession,
    anonymous_id: UUID,
    article_id: int | None,
  ):
    result = await session.execute(
      select(Conversation)
      .where(
        Conversation.anonymous_id == anonymous_id,
        Conversation.article_id == article_id,
      )
    )

    return result.scalar_one_or_none()

  async def create_conversation(
    self, *,
    session: AsyncSession,
    anonymous_id: UUID,
    article_id: int | None
  ):
    conversation = Conversation(
      anonymous_id=anonymous_id,
      article_id=article_id
    )

    session.add(conversation)
    await session.flush() # mengirim perubahan database tanpa melakukan commit di database

    return conversation

  async def get_or_create_conversation(
    self, *,
    session: AsyncSession,
    anonymous_id: UUID,
    article_id: int | None
  ):
    conversation = await self.get_active_conversation(
      session=session,
      anonymous_id=anonymous_id,
      article_id=article_id
    )

    if conversation is not None:
      return conversation

    return await self.create_conversation(
      session=session,
      anonymous_id=anonymous_id,
      article_id=article_id
    )

  async def add_message(
    self, *,
    session: AsyncSession,
    conversation_id: UUID,
    role: str, content: str
  ):
    if role not in {"user", "assistant"}:
      raise ValueError("Invalid message role.")

    if not content.strip():
      raise ValueError("Message content cannot be empty.")

    conversation = await session.get(
      Conversation,
      conversation_id
    )
    
    if conversation is None:
      raise ValueError("Conversation not found.")
    
    message = Message(
      conversation_id=conversation_id,
      role=role,
      content=content
    )

    session.add(message)
    conversation.updated_at = datetime.now(UTC)
    
    return message

  async def get_recent_messages(
    self, *,
    session: AsyncSession,
    conversation_id: UUID, limit: int = 10
  ):
    if limit <= 0:
      raise ValueError("limit must be greater than 0.")

    result = await session.execute(
      select(Message)
      .where(Message.conversation_id == conversation_id)
      .order_by(Message.created_at.desc())
      .limit(limit)
    )

    messages = list(result.scalars().all())
    messages.reverse()

    return messages

  async def delete_conversation(
    self, *,
    session: AsyncSession,
    conversation_id: UUID
  ):
    await session.execute(delete(Conversation).where(Conversation.id == conversation_id))
    await session.commit()

  async def delete_conversation_by_anonymous_id(
    self, *,
    session: AsyncSession,
    anonymous_id: UUID,
  ):
    await session.execute(delete(Conversation).where(Conversation.anonymous_id == anonymous_id))
    await session.commit()

  async def delete_expired_conversations(
    self, *,
    session: AsyncSession,
    ttl_hours: int = 24
  ):
    if ttl_hours <= 0:
      raise ValueError("ttl_hours must be greater than 0.")

    cutoff = datetime.now(UTC) - timedelta(hours=ttl_hours)
    result = await session.execute(
      delete(Conversation).where(
        Conversation.updated_at < cutoff
      )
    )

    await session.commit()
    deleted_count = result.rowcount or 0

    logger.info(
      "Expired conversation cleanup completed. deleted_count=%s",
      deleted_count
    )

    return deleted_count


