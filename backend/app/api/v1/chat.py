import json
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db_session
from app.schemas import ChatRequest, ChatResponse, ChatSource
from app.services import (
  ConversationService,
  EmbeddingService,
  RAGChatService,
  RAGService,
  RAGContextBuilder,
  VectorSearchService
)


router = APIRouter(prefix="/chat", tags=["Chat"])
conversation_service = ConversationService()
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
  session: AsyncSession = Depends(get_db_session),
):
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
    full_answer_parts: list[str] = []
    sources: list[dict] = []

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
            full_answer_parts.append(content)

          data = json.dumps(event, ensure_ascii=False)

          yield f"data: {data}\n\n"

        elif event_type == "sources":
          sources = event.get("sources", [])
          data = json.dumps(event, ensure_ascii=False)

          yield f"data: {data}\n\n"

        elif event_type == "done":
          full_answer = "".join(full_answer_parts).strip()

          if full_answer:
            await conversation_service.add_message(
              session=session,
              conversation_id=conversation.id,
              role="assistant",
              content=full_answer,
              sources=sources,
            )

            await session.commit()

          data = json.dumps(event, ensure_ascii=False)

          yield f"data: {data}\n\n"

    except Exception:
      await session.rollback()
      raise

  return StreamingResponse(
    generate(),
    media_type="text/event-stream",
    headers={
      "Cache-Control": "no-cache",
      "X-Accel-Buffering": "no",
    },
  )
