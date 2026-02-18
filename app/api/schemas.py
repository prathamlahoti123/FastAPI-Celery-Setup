from typing import Any

from pydantic import BaseModel, model_validator


class TaskID(BaseModel):
  """Schema to represent ID of a celery task."""

  id: str


class Task(TaskID):
  """Schema to represent info about celery task."""

  status: str
  result: float | None = None

  @model_validator(mode="before")
  @classmethod
  def validate_result(cls, data: dict[str, Any]) -> dict[str, Any]:
    """Validate result of the task based on its status."""
    if data["status"] != "SUCCESS":
      data["result"] = None
    return data


class TaskData(BaseModel):
  """Schema to represent data to be processed by a task."""

  a: int = 1
  b: int = 1
