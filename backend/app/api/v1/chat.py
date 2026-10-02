import json
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db_session
from app.core import GuestQuotaExceededError
from app.schemas import ChatRequest, ChatResponse, ChatSource
from app.services import (
  ConversationService,
  EmbeddingService,
  RAGChatService,
  RAGService,
  RAGContextBuilder,
  VectorSearchService,
  GuestQuotaService
)


router = APIRouter(prefix="/chat", tags=["Chat"])
conversation_service = ConversationService()
guest_quota_service = GuestQuotaService()
rag_service = RAGService(
  embedding_service=EmbeddingService(),
  vector_search_service=VectorSearchService(),
  context_builder=RAGContextBuilder(),
  chat_service=RAGChatService(),
  conversation_service=conversation_service
)


@router.post("", response_model=ChatResponse)
async def chat(
  request: ChatRequest,
  session: AsyncSession = Depends(get_db_session)
):
  try:
    conversation = await conversation_service.get_or_create_conversation(
      session=session,
      anonymous_id=request.anonymous_id,
      article_id=request.article_id
    )

    result = await rag_service.ask(
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
      content=request.question
    )

    await conversation_service.add_message(
      session=session,
      conversation_id=conversation.id,
      role="assistant",
      content=result.answer
    )

    await session.commit()

    sources = []
    seen_article_ids = set()

    for _, article, _ in result.sources:
      if article.id in seen_article_ids:
        continue

      seen_article_ids.add(article.id)

      sources.append(
        ChatSource(
          article_id=article.id,
          title=article.title,
          source_name=article.source_name,
          image_url=article.image_url,
          url=article.url
        )
      )

    return ChatResponse(
      conversation_id=conversation.id,
      question=request.question,
      answer=result.answer,
      sources=sources
    )
  except Exception:
    await session.rollback()
    raise


@router.post("/stream")
async def chat_stream(
  request: ChatRequest,
  session: AsyncSession = Depends(get_db_session)
):
  try:
    remaining_requests = await guest_quota_service.consume_request(
      session=session,
      anonymous_id=request.anonymous_id,
    )
  except GuestQuotaExceededError as exc:
    await session.rollback()
    raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=str(exc)) from exc

  conversation = await conversation_service.get_or_create_conversation(
    session=session,
    anonymous_id=request.anonymous_id,
    article_id=request.article_id,
  )

  await conversation_service.add_message(
    session=session,
    conversation_id=conversation.id,
    role="user",
    content=request.question,
  )

  await session.commit()

  async def generate():
    assistant_parts = []
    sources = []

    try:
      async for event in rag_service.stream(
        session=session,
        question=request.question,
        conversation_id=conversation.id,
        article_id=request.article_id,
        top_k=3,
      ):
        event_type = event.get("type")

        if event_type == "token":
          content = event.get("content", "")

          if content:
            assistant_parts.append(content)

        elif event_type == "sources":
          sources = event.get("sources", [])

        elif event_type == "done":
          assistant_content = "".join(assistant_parts).strip()

          if assistant_content:
            await conversation_service.add_message(
              session=session,
              conversation_id=conversation.id,
              role="assistant",
              content=assistant_content,
              sources=sources or None,
            )

            await session.commit()

        data = json.dumps(event, ensure_ascii=False)
        yield f"data: {data}\n\n"
    except Exception:
      await session.rollback()
      raise

  response = StreamingResponse(
    generate(),
    media_type="text/event-stream",
  )

  response.headers["X-RateLimit-Limit"] = str(guest_quota_service.MAX_REQUESTS)
  response.headers["X-RateLimit-Remaining"] = str(remaining_requests)

  return response

