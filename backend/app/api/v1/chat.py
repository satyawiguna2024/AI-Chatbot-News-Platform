from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db_session
from app.schemas.chat import ChatRequest, ChatResponse
from app.services import (
  EmbeddingService,
  VectorSearchService,
  RAGContextBuilder,
  RAGChatService,
  RAGService,
)


router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("", response_model=ChatResponse)
async def chat(
  request: ChatRequest,
  session: AsyncSession = Depends(get_db_session),
):
  rag_service = RAGService(
    embedding_service=EmbeddingService(),
    vector_search_service=VectorSearchService(),
    context_builder=RAGContextBuilder(),
    chat_service=RAGChatService()
  )

  answer = await rag_service.ask(
    session=session,
    question=request.question,
    article_id=request.article_id,
    limit=5
  )

  return ChatResponse(answer=answer)