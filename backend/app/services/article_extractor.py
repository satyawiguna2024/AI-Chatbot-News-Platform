from dataclasses import dataclass
from trafilatura import bare_extraction, fetch_url


@dataclass
class ExtractedArticle:
  title: str | None
  description: str | None
  author: str | None
  published_at: str | None
  content: str


class ArticleExtractor:
  async def extract(self, url: str):
    downloaded = fetch_url(url)

    if not downloaded:
      raise ValueError(f"Failed to download article: {url}")

    document = bare_extraction(downloaded, with_metadata=True, url=url)

    # print("\n\nDEBUG DOCUMENTS -> ", document.text)
    
    if document is None:
      raise ValueError(f"Failed to extract article: {url}")

    if not document.text:
      raise ValueError(f"Article content is empty: {url}")

    return ExtractedArticle(
      title=document.title,
      description=document.description,
      author=document.author,
      published_at=document.date,
      content=document.text,
    )