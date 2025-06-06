from pydantic import BaseModel


class TaskID(BaseModel):
  """Schema to represent ID of a celery task"""
  id: str


class Task(TaskID):
  """Schema to represent info about celery task"""
  status: str
  result: int | None = None # bg task returns int as a result
