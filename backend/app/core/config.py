from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
  app_name: str = Field(default="AI Chatbot News Platform")
  app_env: str = Field(default="development")
  database_url: str
  news_api_key: str
  openai_api_key: str
  openrouter_api_key: str
  openrouter_base_url: str = Field(default="https://openrouter.ai/api/v1")
  openrouter_model: str = Field(default="cohere/north-mini-code:free")

  model_config = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
    case_sensitive=False,
    extra="ignore",
  )


@lru_cache
def get_settings():
  return Settings()