from celery.result import AsyncResult  # noqa: I001
from fastapi import APIRouter

from api.schemas import Task, TaskID, TaskData
from api.tasks import some_complex_task


router = APIRouter()


@router.get(
  "/tasks/{task_id}",
  description="Status and result of a celery task",
)
def get_task_status(task_id: str) -> Task:
  """Get info about celery task."""
  res = AsyncResult(task_id)
  return Task(id=res.id, status=res.status, result=res.result)


@router.post(
  "/tasks/run",
  description="Run a background task",
)
def run_task(data: TaskData) -> TaskID:
  """Endpoint to run a 'CPU-intensive' background task."""
  task: AsyncResult = some_complex_task.delay(data.a, data.b)
  return TaskID(id=task.id)
