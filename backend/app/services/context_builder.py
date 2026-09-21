import tiktoken
from app.models import Article, ArticleChunk


class RAGContextBuilder:
  def __init__(self, *, max_tokens: int = 1500):
    if max_tokens <= 0:
      raise ValueError("max_tokens must be greater than 0.")

    self.max_tokens = max_tokens
    self.encoding = tiktoken.get_encoding("cl100k_base")

  def build(self, results: list[tuple[ArticleChunk, Article, float]]):
    if not results:
      return ""

    context_parts: list[str] = []
    current_tokens = 0

    for chunk, article, distance in results:
      chunk_text = (
        f"[Article]\n"
        f"Title: {article.title}\n"
        f"Source: {article.source_name or 'Unknown'}\n"
        f"URL: {article.url}\n"
        f"Chunk: {chunk.chunk_index}\n"
        f"Content:\n{chunk.content}"
      )

      chunk_tokens = len(self.encoding.encode(chunk_text))

      # Jangan masukkan chunk jika melewati budget.
      if current_tokens + chunk_tokens > self.max_tokens:
        break

      context_parts.append(chunk_text)
      current_tokens += chunk_tokens

    return "\n\n".join(context_parts)