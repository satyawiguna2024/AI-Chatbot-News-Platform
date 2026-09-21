from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import ArticleChunk, Article


class VectorSearchService:
  async def search_similar_chunks(
    self, *,
    session: AsyncSession,
    query_embedding: list[float],
    article_id: int | None = None,
    top_k: int = 3
  ):
    if not query_embedding:
      raise ValueError("Query embedding cannot be empty.")

    if top_k <= 0:
      raise ValueError("top_k must be greater than 0.")

    # Menghitung cosine distance antara query dan setiap chunk.
    distance = ArticleChunk.embedding.cosine_distance(query_embedding)
    query = (
      select(ArticleChunk, Article, distance.label("distance"))
      .join(Article, Article.id == ArticleChunk.article_id)
      .where(ArticleChunk.embedding.is_not(None))
    )

    if article_id is not None:
      query = query.where(ArticleChunk.article_id == article_id)

    # Menghasilkan nilai jarak.
    # Makin dekat angkanya ke 0, artinya makna kedua teks makin serupa/relevan.
    query = (query.order_by(distance).limit(top_k))
    result = await session.execute(query)
    return result.all()