from uuid import UUID, uuid4
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db_session
from app.services import ConversationService
from app.schemas import (
  ConversationCreateRequest,
  ConversationCreateResponse,
  ConversationContextRequest,
  ConversationContextResponse,
  ConversationMessageResponse
)

router = APIRouter(prefix="/conversation", tags=["Conversation"])
conversation_service = ConversationService()
anonymous_id = uuid4()

@router.get("/context", response_model=ConversationContextResponse)
async def get_conversation_context(
  anonymous_id: UUID,
  article_id: int | None = None,
  session: AsyncSession = Depends(get_db_session),
):
  conversation = await conversation_service.get_conversation_context(
    session=session,
    anonymous_id=anonymous_id,
    article_id=article_id,
  )

  if conversation is None:
    return ConversationContextResponse(
      conversation_id=None,
      anonymous_id=anonymous_id,
      article_id=article_id,
      messages=[],
    )

  messages = await conversation_service.get_messages(
    session=session,
    conversation_id=conversation.id,
  )

  return ConversationContextResponse(
    conversation_id=conversation.id,
    anonymous_id=conversation.anonymous_id,
    article_id=conversation.article_id,
    messages=[
      ConversationMessageResponse(
        id=message.id,
        role=message.role,
        content=message.content,
        sources=message.sources,
      )
      for message in messages
    ],
  )

@router.post("", response_model=ConversationCreateResponse)
async def create_conversation(
  # request: ConversationCreateRequest,
  session: AsyncSession = Depends(get_db_session),
):
  try:
    # conversation = await conversation_service.create_conversation(
    #   session=session,
    #   anonymous_id=request.anonymous_id,
    #   article_id=request.article_id
    # )
    
    # create annonymous_id
    conversation = await conversation_service.create_conversation(
      session=session,
      anonymous_id=anonymous_id,
      article_id=1
    )

    await session.commit()

    return ConversationCreateResponse(
      conversation_id=conversation.id,
      anonymous_id=conversation.anonymous_id,
      article_id=conversation.article_id
    )
  except Exception:
    await session.rollback()
    raise

@router.delete("")
async def delete_conversation(
  request: ConversationContextRequest,
  session: AsyncSession = Depends(get_db_session)
):
  await conversation_service.delete_conversation_by_anonymous_id(
    session=session,
    anonymous_id=request.anonymous_id
  )

  return {"status": "deleted"}
