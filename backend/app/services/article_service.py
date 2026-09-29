from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Article, ArticleChunk
from app.schemas import NewsAPIArticle
from app.services.article_extractor import ArticleExtractor
from app.services.article_normalizer import normalize_article
from app.services.translator import ArticleTranslator
from app.services.content_cleaner import ArticleContentCleaner
from app.services.content_chunker import ArticleContentChunker
from app.services.embedding import EmbeddingService


class ArticleService:
  def __init__(
    self, *,
    extractor: ArticleExtractor,
    translator: ArticleTranslator,
    cleaner: ArticleContentCleaner,
    chunker: ArticleContentChunker,
    embedding: EmbeddingService
  ):
    self.extractor = extractor
    self.translator = translator
    self.cleaner = cleaner
    self.chunker = chunker
    self.embedding = embedding

  async def ingest_article(
    self, *,
    session: AsyncSession,
    news_article: NewsAPIArticle
  ):
    result = await session.execute(
      select(Article).where(
        Article.url == news_article.url
      )
    )

    existing_article = result.scalar_one_or_none()
    if existing_article:
      return existing_article

    article = normalize_article(news_article)

    
    extracted = await self.extractor.extract(news_article.url)
    if extracted.title:
      article.title = extracted.title

    article.content = self.cleaner.clean(extracted.content)
    
    translated = await self.translator.translate_to_indonesian(
      title=article.title,
      description=article.description,
      content=article.content
    )

    # memasuki hasil translation ke model database.
    article.translated_title = translated.title
    article.translated_description = translated.description
    article.translated_content = translated.content
    article.translated_language = "id" # bahasa indonesia

    session.add(article)

    # flush()?
    # disini bertujuan untuk mengambil id nya tanpa harus memerlukan commit terlebih dahulu.
    await session.flush()
    
    chunks = self.chunker.chunk(article.content)
    for chunk in chunks:
      embedding = await self.embedding.embed_text(chunk.content)
      
      article_chunk = ArticleChunk(
        article_id=article.id,
        chunk_index=chunk.index,
        content=chunk.content,
        token_count=chunk.token_count,
        embedding=embedding
      )
      session.add(article_chunk)
    
    await session.commit()
    await session.refresh(article)
    
    return article

  async def get_articles(
    self, *,
    session: AsyncSession,
    page: int,
    limit: int,
  ):
    offset = (page - 1) * limit
    total_result = await session.execute(select(func.count()).select_from(Article))
    total = total_result.scalar_one()

    result = await session.execute(
      select(Article)
      .order_by(
        Article.published_at.desc().nullslast(),
        Article.id.desc(),
      )
      .offset(offset)
      .limit(limit)
    )

    articles = list(result.scalars().all())

    return articles, total

  async def get_article_by_id(
    self, *,
    session: AsyncSession,
    article_id: int,
  ):
    result = await session.execute(select(Article).where(Article.id == article_id))
    
    return result.scalar_one_or_none()
