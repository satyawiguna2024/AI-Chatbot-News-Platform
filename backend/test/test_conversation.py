from uuid import uuid4
import pytest
import pytest_asyncio
from sqlalchemy import select

from app.db import AsyncSessionLocal
from app.models import Conversation
from app.services.conversation import ConversationService


# pytest fixture db session
@pytest_asyncio.fixture
async def db_session():
  async with AsyncSessionLocal() as session:
    yield session


@pytest.mark.asyncio
async def test_conversation_service(db_session):
    service = ConversationService()
    anonymous_id = uuid4()

    # Buat conversation untuk sebuah article.
    conversation = await service.create_conversation(
      session=db_session,
      anonymous_id=anonymous_id,
      article_id=1,
    )

    assert conversation.id is not None
    print(f"\nmemastikan ada conversation.id: {conversation.id}")
    assert conversation.anonymous_id == anonymous_id
    print(f"\nmemastikan conversation.anonymous_id sama dengan anonymous_id: {conversation.anonymous_id == anonymous_id}")
    assert conversation.article_id == 1
    print(f"\nmemastikan ada conversation.article_id sama dengan 1: {conversation.article_id == 1}")

    # Simpan pesan user.
    user_message = await service.add_message(
      session=db_session,
      conversation_id=conversation.id,
      role="user",
      content="Apa itu BUK Migas?"
    )

    assert user_message.role == "user"
    print(f"\nmemastikan ada user_message.role sama dengan user: {user_message.role == 'user'}")

    # Simpan jawaban assistant.
    assistant_message = await service.add_message(
      session=db_session,
      conversation_id=conversation.id,
      role="assistant",
      content="BUK Migas adalah ..."
    )

    assert assistant_message.role == "assistant"
    print(f"\nmemastikan ada user_message.role sama dengan assistant: {assistant_message.role == 'assistant'}")

    # Ambil conversation yang sudah ada.
    existing = await service.get_active_conversation(
      session=db_session,
      anonymous_id=anonymous_id,
      article_id=1
    )

    assert existing is not None
    print(f"\nmemastikan conversation itu benar-benar ada atau active: {existing}")
    assert existing.id == conversation.id
    print(f"\nmemastikan conversation itu benar-benar sama dengan variable conversation.id: {existing.id == conversation.id}")

    # Ambil message terbaru.
    messages = await service.get_recent_messages(
      session=db_session,
      conversation_id=conversation.id,
      limit=10
    )

    assert len(messages) == 2
    print(f"\nmemastikan panjang pesan itu sama dengan 2: {len(messages) == 2}")
    assert messages[0].role == "user"
    print(f"\nrole user: {messages[0].role == 'user'}")
    assert messages[1].role == "assistant"
    print(f"\nrole assistant: {messages[1].role == 'assistant'}")

    # Pastikan conversation dan message benar-benar ada.
    result = await db_session.execute(select(Conversation).where(Conversation.id == conversation.id))
    saved_conversation = result.scalar_one_or_none()
    
    assert saved_conversation is not None
    print(f"\nmemastikan conversation tersimpan dengan baik: {saved_conversation}")