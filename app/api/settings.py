from functools import lru_cache
from typing import TypedDict

from pydantic import Field
from pydantic_settings import BaseSettings


class FastAPIKwargs(TypedDict):
  """Kwargs for FastAPI app."""

  title: str
  description: str
  version: str
  debug: bool


class Settings(BaseSettings):
  """API settings."""

  title: str = Field("FastAPI Celery Example", env="API_TITLE")
  description: str = Field(
    "Example of FastAPI and Celery integration.",
    env="API_DESCRIPTION",
  )
  version: str = Field("0.0.1", env="API_VERSION")
  debug: bool = Field(False, env="API_DEBUG")

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
