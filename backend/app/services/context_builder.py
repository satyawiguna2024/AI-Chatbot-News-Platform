from app.models import ArticleChunk


class RAGContextBuilder:
  def build(self, results: list[tuple[ArticleChunk, float]]):
    if not results:
      return ""

    context_parts: list[str] = []
    
    # print("\n\n\nDEBUG -> result, context_builder service: ", results)

    for chunk, distance in results:
      context_parts.append(
        f"[Article Chunk {chunk.chunk_index}]\n"
        f"{chunk.content}"
      )

    return "\n\n".join(context_parts)