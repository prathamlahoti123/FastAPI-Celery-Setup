from pydantic import BaseModel


class TaskID(BaseModel):
  """Schema to represent ID of a celery task"""
  id: str


class Task(TaskID):
  """Schema to represent info about celery task"""
  status: str
  result: float | None = None # bg task returns float as a result
