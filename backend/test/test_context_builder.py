import pytest
from sqlalchemy import select

from app.db import AsyncSessionLocal
from app.models import ArticleChunk
from app.services import RAGContextBuilder


@pytest.mark.asyncio
async def test_context_builder():
    context_builder = RAGContextBuilder()

    async with AsyncSessionLocal() as session:
      result = await session.execute(
        select(ArticleChunk)
        .where(ArticleChunk.article_id == 3)
        .order_by(ArticleChunk.chunk_index)
      )

      chunks = result.scalars().all()

    results = [
      (chunk, 0.4)
      for chunk in chunks
    ]

    context = context_builder.build(results)
    print("\n\n\n=== RAG CONTEXT ===")
    print(context)

    assert context
    assert "[Article Chunk 0]" in context