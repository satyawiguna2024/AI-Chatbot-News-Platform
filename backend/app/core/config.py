from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
  app_name: str = Field(default="AI Chatbot News Platform")
  app_env: str = Field(default="development")
  cors_allowed_origins: list[str] = Field(default_factory=list)
  database_url: str
  news_api_key: str
  openai_api_key: str

  model_config = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
    case_sensitive=False,
    extra="ignore",
  )


@lru_cache
def get_settings():
  return Settings()