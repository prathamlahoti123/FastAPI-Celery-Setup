from pydantic import BaseModel


class TaskID(BaseModel):
  """Schema to represent ID of a celery task."""

  id: str


class Task(TaskID):
  """Schema to represent info about celery task."""

  status: str
  result: float | None = None


class TaskData(BaseModel):
  """Schema to represent data to be processed by a task."""

  a: int = 1
  b: int = 1
