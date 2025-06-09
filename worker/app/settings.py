from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
  """Settings of the worker app."""
  celery_broker_url: str = "redis://redis:6379/1"
  celery_result_backend: str = "redis://redis:6379/2"


@lru_cache
def get_settings() -> Settings:
  """Return cached project settings."""
  return Settings()


settings = get_settings()
