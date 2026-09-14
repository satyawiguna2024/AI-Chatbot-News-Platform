from app.services import ArticleContentCleaner


def test_clean_article_content():
  cleaner = ArticleContentCleaner()
  content = """The first paragraph of the article.

  The second paragraph contains important information.

  The final paragraph contains the actual news.

  Related news: Another article
  Related news: Another article
  Translator: John Doe
  Editor: Jane Doe
  Copyright © ANTARA 2026
  """

  cleaned = cleaner.clean(content)

  print("\n=== CLEANED CONTENT ===")
  print(cleaned)

  assert "The first paragraph" in cleaned
  assert "The second paragraph" in cleaned
  assert "The final paragraph" in cleaned

  assert "Related news:" not in cleaned
  assert "Translator:" not in cleaned
  assert "Editor:" not in cleaned
  assert "Copyright ©" not in cleaned