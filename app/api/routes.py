from celery.result import AsyncResult
from fastapi import APIRouter

from api.schemas import Task


router = APIRouter()


@router.get(
  "/tasks/{id}",
  description="Status and result of a celery task",
  response_model=Task
)
def get_task_status(id: str) -> Task:
  """Get info about celery task"""
  res = AsyncResult(id)
  return Task(id=id, status=res.status, result=res.result)
