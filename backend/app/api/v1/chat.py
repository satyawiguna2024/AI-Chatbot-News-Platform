from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db_session
from app.schemas import ChatRequest, ChatResponse, ConversationContextRequest
from app.services import (
  EmbeddingService,
  VectorSearchService,
  RAGContextBuilder,
  RAGChatService,
  RAGService,
  ConversationService
)


router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("", response_model=ChatResponse)
async def chat(
  request: ChatRequest,
  session: AsyncSession = Depends(get_db_session)
):
  conversation_service = ConversationService()
  rag_service = RAGService(
    embedding_service=EmbeddingService(),
    vector_search_service=VectorSearchService(),
    context_builder=RAGContextBuilder(),
    chat_service=RAGChatService(),
    conversation_service=conversation_service,
  )
  
  try:
    conversation = await conversation_service.get_or_create_conversation(
      session=session,
      anonymous_id=request.anonymous_id,
      article_id=request.article_id
    )
    
    answer = await rag_service.ask(
      session=session,
      question=request.question,
      conversation_id=conversation.id,
      article_id=request.article_id,
      top_k=3
    )
    
    await conversation_service.add_message(
      session=session,
      conversation_id=conversation.id,
      role="user",
      content=request.question,
    )
    
    await conversation_service.add_message(
      session=session,
      conversation_id=conversation.id,
      role="assistant",
      content=answer,
    )
    
    await session.commit()
    
    return ChatResponse(
      conversation_id=conversation.id,
      answer=answer
    )
    
  except Exception:
    await session.rollback()
    raise


@router.delete("/conversation")
async def delete_conversation(
  request: ConversationContextRequest,
  session: AsyncSession = Depends(get_db_session),
):
  conversation_service = ConversationService()
  await conversation_service.delete_conversation_by_anonymous_id(
    session=session,
    anonymous_id=request.anonymous_id,
  )

  return {"status": "deleted"}

# @router.post("", response_model=ChatResponse)
# async def chat(
#   request: ChatRequest,
#   session: AsyncSession = Depends(get_db_session),
# ):
#   rag_service = RAGService(
#     embedding_service=EmbeddingService(),
#     vector_search_service=VectorSearchService(),
#     context_builder=RAGContextBuilder(),
#     chat_service=RAGChatService()
#   )

#   answer = await rag_service.ask(
#     session=session,
#     question=request.question,
#     article_id=request.article_id,
#     limit=5
#   )

#   return ChatResponse(answer=answer)

