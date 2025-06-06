from celery.result import AsyncResult
from fastapi import APIRouter

from api.schemas import Task, TaskID
from api.tasks import some_complex_task


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


@router.post(
  "/tasks/run",
  description="Run a background task",
  response_model=TaskID
)
async def run_task(a: int, b: int) -> TaskID:
  """Endpoint to run a 'CPU-intensive' background task"""
  task: AsyncResult = some_complex_task.delay(a, b)
  return TaskID(id=task.id)
