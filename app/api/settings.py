from functools import lru_cache
from typing import TypedDict

from pydantic_settings import BaseSettings


class FastAPIKwargs(TypedDict):
  """Kwargs for FastAPI app."""

  title: str
  description: str
  version: str
  debug: bool


class Settings(BaseSettings):
  """API settings."""

  title: str = "FastAPI Celery Example"
  description: str = "Example of FastAPI and Celery integration."
  version: str = "0.0.1"
  debug: bool = False

  @property
  def fastapi_kwargs(self) -> FastAPIKwargs:
    """Kwargs for FastAPI app."""
    return FastAPIKwargs(
      title=self.title,
      description=self.description,
      version=self.version,
      debug=self.debug,
    )


@lru_cache
def get_settings() -> Settings:
  """Return cached project settings."""
  return Settings()


settings = get_settings()
