from app.models import Article
from app.schemas import NewsAPIArticle


def normalize_article(article: NewsAPIArticle):
  return Article(
    title=article.title,
    description=article.description,
    content=article.content,
    url=article.url,
    source_name=article.source.name,
    author=article.author,
    published_at=article.publishedAt,
    image_url=article.urlToImage
  )