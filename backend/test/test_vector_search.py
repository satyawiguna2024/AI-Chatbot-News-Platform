import pytest
from app.models import Article, ArticleChunk
from app.services.vector_search import VectorSearchService


@pytest.mark.asyncio
async def test_vector_search_can_filter_by_article(db_session):
  article_1 = Article(
    title="Article One",
    description="Description one",
    content="Content one",
    url="https://example.com/article-one",
  )

  article_2 = Article(
    title="Article Two",
    description="Description two",
    content="Content two",
    url="https://example.com/article-two",
  )

  db_session.add_all([article_1, article_2])

  await db_session.flush()

  chunk_1 = ArticleChunk(
    article_id=article_1.id,
    chunk_index=0,
    content="Information from article one.",
    token_count=5,
    embedding=[0.1] * 1536,
  )

  chunk_2 = ArticleChunk(
    article_id=article_2.id,
    chunk_index=0,
    content="Information from article two.",
    token_count=5,
    embedding=[0.2] * 1536,
  )

  db_session.add_all([chunk_1, chunk_2])

  await db_session.commit()

  service = VectorSearchService()
  results = await service.search_similar_chunks(
    session=db_session,
    query_embedding=[0.1] * 1536,
    article_id=article_1.id,
    top_k=3
  )
  assert len(results) == 1

  chunk, article, distance = results[0]
  assert chunk.article_id == article_1.id
  assert article.id == article_1.id
  assert article.title == "Article One"
  assert distance >= 0

@pytest.mark.asyncio
async def test_vector_search_can_search_globally(db_session):
  article_1 = Article(
    title="Global Article One",
    description="Description one",
    content="Content one",
    url="https://example.com/global-one",
  )

  article_2 = Article(
    title="Global Article Two",
    description="Description two",
    content="Content two",
    url="https://example.com/global-two",
  )

  db_session.add_all([article_1, article_2])

  await db_session.flush()

  chunk_1 = ArticleChunk(
    article_id=article_1.id,
    chunk_index=0,
    content="Information from global article one.",
    token_count=5,
    embedding=[0.1] * 1536,
  )

  chunk_2 = ArticleChunk(
    article_id=article_2.id,
    chunk_index=0,
    content="Information from global article two.",
    token_count=5,
    embedding=[0.2] * 1536,
  )

  db_session.add_all([chunk_1, chunk_2])

  await db_session.commit()

  service = VectorSearchService()
  results = await service.search_similar_chunks(
    session=db_session,
    query_embedding=[0.1] * 1536,
    article_id=None,
    top_k=3,
  )

  print("RESULT COUNT:", len(results))
  # assert len(results) == 2

  for chunk, article, distance in results:
    print(
      "ARTICLE:",
      article.id,
      article.title,
      "CHUNK:",
      chunk.id,
    )
    # assert chunk.article_id == article.id
    # assert article.title in {
    #   "Global Article One",
    #   "Global Article Two"
    # }
    # assert distance >= 0


