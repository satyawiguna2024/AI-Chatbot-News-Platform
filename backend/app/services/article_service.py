from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Article
from app.schemas import NewsAPIArticle
from app.services import ArticleExtractor, normalize_article, ArticleTranslator


class ArticleService:
  def __init__(
    self, *,
    extractor: ArticleExtractor,
    translator: ArticleTranslator,
    cleaner: ArticleTranslator
  ):
    self.extractor = extractor
    self.translator = translator
    self.cleaner = cleaner

  async def ingest_article(
    self, *,
    session: AsyncSession, news_article: NewsAPIArticle,
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

    article.content = self.cleaner.client(extracted.content)
    
    translated = await self.translator.translate_to_indonesian(
      title=article.title,
      description=article.description,
      content=article.content
    )

    # memasuki hasil translation ke model database.
    article.translated_title = translated.title
    article.translated_description = translated.description
    article.translated_content = translated.content
    article.translated_language = "id"

    session.add(article)
    await session.commit()
    await session.refresh(article)

    return article