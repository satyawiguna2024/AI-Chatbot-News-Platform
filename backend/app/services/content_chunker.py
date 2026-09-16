import re
import tiktoken
from dataclasses import dataclass


@dataclass
class ArticleChunk:
  index: int
  content: str
  token_count: int


class ArticleContentChunker:
  def __init__(
    self, *,
    max_tokens: int = 600,
    overlap_tokens: int = 80
  ):
    if overlap_tokens >= max_tokens:
      raise ValueError("overlap_tokens must be smaller than max_tokens.")

    self.max_tokens = max_tokens
    self.overlap_tokens = overlap_tokens
    self.encoding = tiktoken.get_encoding("cl100k_base")

  def chunk(self, content: str):
    if not content.strip():
      return []

    paragraphs = self._split_paragraphs(content)
    chunks: list[ArticleChunk] = []
    current_paragraphs: list[str] = []
    current_tokens = 0

    for paragraph in paragraphs:
      paragraph_tokens = self._count_tokens(paragraph)

      # Kalau paragraf sendiri terlalu besar,
      # kita pecah berdasarkan token.
      if paragraph_tokens > self.max_tokens:
        if current_paragraphs:
          chunks.append(
            self._create_chunk(
              index=len(chunks),
              paragraphs=current_paragraphs,
            )
          )

          current_paragraphs = []
          current_tokens = 0

        large_chunks = self._split_large_paragraph(paragraph)

        for large_chunk in large_chunks:
          chunks.append(
            ArticleChunk(
              index=len(chunks),
              content=large_chunk,
              token_count=self._count_tokens(large_chunk)
            )
          )

        continue

      # Kalau paragraf masih bisa masuk ke chunk sekarang.
      if current_tokens + paragraph_tokens <= self.max_tokens:
        current_paragraphs.append(paragraph)
        current_tokens += paragraph_tokens
        continue

      # Chunk sekarang sudah penuh.
      chunks.append(
        self._create_chunk(
          index=len(chunks),
          paragraphs=current_paragraphs,
        )
      )

      # Ambil beberapa token terakhir sebagai overlap.
      overlap_text = self._create_overlap(current_paragraphs)
      if overlap_text:
        current_paragraphs = [overlap_text]
        current_tokens = self._count_tokens(overlap_text)
      else:
        current_paragraphs = []
        current_tokens = 0

      # Masukkan paragraf baru.
      current_paragraphs.append(paragraph)
      current_tokens += paragraph_tokens

    # Jangan lupa chunk terakhir.
    if current_paragraphs:
      chunks.append(
        self._create_chunk(
          index=len(chunks),
          paragraphs=current_paragraphs,
        )
      )

    return chunks

  def _split_paragraphs(self, content: str):
    paragraphs = re.split(r"\n\s*\n", content)

    return [
      paragraph.strip()
      for paragraph in paragraphs
      if paragraph.strip()
    ]

  def _count_tokens(self, text: str):
    return len(self.encoding.encode(text))

  def _create_chunk(
    self, *, index: int,
    paragraphs: list[str]
  ):
    content = "\n\n".join(paragraphs)

    return ArticleChunk(
      index=index,
      content=content,
      token_count=self._count_tokens(content),
    )

  def _create_overlap(self, paragraphs: list[str]):
    overlap_parts: list[str] = []
    token_count = 0

    for paragraph in reversed(paragraphs):
      paragraph_tokens = self._count_tokens(paragraph)

      if token_count + paragraph_tokens > self.overlap_tokens:
        break

      overlap_parts.insert(0, paragraph)
      token_count += paragraph_tokens

    return "\n\n".join(overlap_parts)

  def _split_large_paragraph(self, paragraph: str):
    tokens = self.encoding.encode(paragraph)
    chunks: list[str] = []
    start = 0

    while start < len(tokens):
      end = min(
        start + self.max_tokens,
        len(tokens),
      )

      chunk_tokens = tokens[start:end]
      chunks.append(self.encoding.decode(chunk_tokens))
      
      if end >= len(tokens):
        break

      start = end - self.overlap_tokens

    return chunks