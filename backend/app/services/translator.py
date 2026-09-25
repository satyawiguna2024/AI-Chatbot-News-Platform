from openai import AsyncOpenAI
from pydantic import BaseModel
from app.core import get_settings

class TranslatedArticle(BaseModel):
  title: str
  description: str
  content: str

class ArticleTranslator:
  def __init__(self):
    settings = get_settings()
    self.client = AsyncOpenAI(base_url=settings.openrouter_base_url, api_key=settings.openrouter_api_key)

  async def translate_to_indonesian(
    self, *, title: str,
    description: str | None, content: str | None,
  ):
    prompt_system="""
    You are a professional English to Indonesian
    news translator. Translate faithfully.
    Do not summarize or add information.
    """
    
    prompt = f"""
    Translate the following English news article into natural Indonesian.

    Rules:
    - Preserve the original meaning.
    - Do not add information.
    - Do not summarize.
    - Keep names, organizations, places, and numbers accurate.
    - Return only the translated article in the requested format.
    
    IMPORTANT:
    - Translate TITLE only into the "title" field.
    - Translate DESCRIPTION only into the "description" field.
    - Translate CONTENT only into the "content" field.
    - Do NOT include labels such as "TITLE:", "DESCRIPTION:", "CONTENT:",
      "JUDUL:", "DESKRIPSI:", or "ISI:" inside any field.
    - Do not summarize.
    - Do not add information.
    - Preserve the original meaning.
    - Preserve names, organizations, places, and numbers.
    
    TITLE:
    {title}

    DESCRIPTION:
    {description or ""}

    CONTENT:
    {content or ""}
    """
    
    response_output_format={
      "type": "json_schema",
      "json_schema": {
        "name": "translated_article",
        "strict": True,
        "schema": {
          "type": "object",
          "properties": {
              "title": {
                "type": "string",
                "description": "The translated Indonesian title.",
              },
              "description": {
                "type": "string",
                "description": "The translated Indonesian description.",
              },
              "content": {
                "type": "string",
                "description": "The translated Indonesian content.",
              },
          },
          "required": [
            "title",
            "description",
            "content",
          ],
          "additionalProperties": False,
        },
      },
    }

    response = await self.client.chat.completions.create(
      model= "nex-agi/nex-n2.5-mini:free",
      response_format=response_output_format,
      stream=False,
      messages=[
        {
          "role": "system",
          "content": prompt_system
        },
        {
          "role": "user",
          "content": prompt
        }
      ]
    )
  
    # print("\n\n\nDEBUG TRANSLATOR -> ", response)
    
    message = response.choices[0].message
    
    
    if not message.content:
      raise ValueError("Translation model returned empty content.")
    
    print("\n=== TRANSLATOR DEBUG ===")
    print("finish_reason:", response.choices[0].finish_reason)
    print("content length:", len(message.content))
    print("content:", message.content)

    return TranslatedArticle.model_validate_json(message.content)
  
