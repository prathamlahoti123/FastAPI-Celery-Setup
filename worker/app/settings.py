from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
  """Settings of the app"""
  celery_broker_url: str
  celery_result_backend: str


@lru_cache
def get_settings() -> Settings:
  """Return cached project settings."""
  return Settings()


settings = get_settings()
