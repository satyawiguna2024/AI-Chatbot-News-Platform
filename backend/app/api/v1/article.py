from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db_session
from app.schemas import ArticleDetailResponse, ArticleListItem, ArticleListResponse
from app.services import (
  ArticleService,
  ArticleExtractor,
  ArticleTranslator,
  ArticleContentCleaner,
  ArticleContentChunker,
  EmbeddingService
)


router = APIRouter(prefix="/articles", tags=["Articles"])
article_service = ArticleService(
  extractor=ArticleExtractor,
  translator=ArticleTranslator,
  cleaner=ArticleContentCleaner,
  chunker=ArticleContentChunker,
  embedding=EmbeddingService
)


@router.get("", response_model=ArticleListResponse)
async def get_articles(
  page: int = Query(default=1, ge=1),
  limit: int = Query(default=12, ge=1, le=50),
  session: AsyncSession = Depends(get_db_session)
):
  articles, has_next = await article_service.get_articles(
    session=session,
    page=page,
    limit=limit,
  )

  return ArticleListResponse(
    items=[
      ArticleListItem(
        id=article.id,
        title=article.title,
        translated_title=article.translated_title,
        description=article.description,
        translated_description=article.translated_description,
        source_name=article.source_name,
        author=article.author,
        published_at=article.published_at,
        image_url=article.image_url,
        url=article.url,
      )
      for article in articles
    ],
    page=page,
    limit=limit,
    has_next=has_next,
  )


@router.get("/{article_id}", response_model=ArticleDetailResponse)
async def get_article(
  article_id: int,
  session: AsyncSession = Depends(get_db_session)
):
  article = await article_service.get_article_by_id(
    session=session,
    article_id=article_id,
  )

  if article is None:
    raise HTTPException(
      status_code=404,
      detail="Article not found.",
    )

  return ArticleDetailResponse(
    id=article.id,
    title=article.title,
    description=article.description,
    content=article.content,
    translated_title=article.translated_title,
    translated_description=article.translated_description,
    translated_content=article.translated_content,
    translated_language=article.translated_language,
    source_name=article.source_name,
    author=article.author,
    published_at=article.published_at,
    image_url=article.image_url,
    url=article.url,
    created_at=article.created_at,
  )