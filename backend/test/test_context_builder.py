import tiktoken

from app.models import ArticleChunk
from app.services import RAGContextBuilder


def test_context_builder_respects_token_budget():
  encoding = tiktoken.get_encoding("cl100k_base")

  chunks = [
    ArticleChunk(
      id=1,
      article_id=1,
      chunk_index=0,
      content="Indonesia memiliki banyak wilayah pesisir.",
      token_count=10,
    ),
    ArticleChunk(
      id=2,
      article_id=1,
      chunk_index=1,
      content="Pemerintah mengembangkan ekonomi masyarakat pesisir.",
      token_count=10,
    ),
  ]

  results = [
    (chunks[0], 0.2),
    (chunks[1], 0.3),
  ]

  builder = RAGContextBuilder(max_tokens=20)
  context = builder.build(results)

  actual_tokens = len(encoding.encode(context))
  print(f"actual_tokens: {actual_tokens}")
  assert actual_tokens <= 20