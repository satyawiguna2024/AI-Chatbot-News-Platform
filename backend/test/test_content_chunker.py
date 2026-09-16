from app.services.content_chunker import ArticleContentChunker


def test_article_content_chunker():
    content = """
    Indonesia's government announced a new policy today.
    The policy will affect several sectors across the country.
    Officials said the implementation will begin next month.
    The government expects the policy to improve economic growth.
    Several industry groups welcomed the announcement.
    """

    chunker = ArticleContentChunker(max_tokens=30, overlap_tokens=5)
    chunks = chunker.chunk(content)

    assert len(chunks) > 1

    for chunk in chunks:
      assert chunk.content
      assert chunk.token_count > 0

      print(f"\n=== CHUNK {chunk.index} ===")
      print(f"Tokens: {chunk.token_count}")
      print(chunk.content)