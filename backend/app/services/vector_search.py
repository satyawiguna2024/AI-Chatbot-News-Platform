from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import ArticleChunk


class VectorSearchService:
  async def search_similar_chunks(
    self, *,
    session: AsyncSession, query_embedding: list[float],
    article_id: int | None = None, limit: int = 5
  ):
    
    # cosine:
    # Membandingkan arah sudut dari dua vektor embedding (vektor pertanyaan user vs vektor teks di database).
    query = select(
      ArticleChunk,
      ArticleChunk.embedding.cosine_distance(query_embedding)
      .label("distance")).where(ArticleChunk.embedding.is_not(None)
    )

    # Jika article_id ada (tidak bernilai None)
    if article_id is not None:
      query = query.where(ArticleChunk.article_id == article_id)

    # Menghasilkan nilai jarak.
    # Makin dekat angkanya ke 0, artinya makna kedua teks makin serupa/relevan.
    query = query.order_by("distance").limit(limit)
    result = await session.execute(query)

    return result.all()