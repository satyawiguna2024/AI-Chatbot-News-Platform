import pytest
from app.services import ArticleTranslator


@pytest.mark.asyncio
async def test_translate_article():
  translator = ArticleTranslator()

  translated = await translator.translate_to_indonesian(
    title="Indonesia launches new economic policy",
    description="The government announced a new economic policy.",
    content=(
      "The Indonesian government announced a new economic "
      "policy on Monday to support economic growth."
    ),
  )
  print("\n\n\nDEBUG TRANSLATED -> ", translated)
  
  print("\n\n=== TRANSLATION RESULT ===")

  print(f"\nTitle       : {translated.title}")
  print(f"Description : {translated.description}")
  print(f"Content     : {translated.content}")

  assert translated.title
  assert translated.description
  assert translated.content