from celery.result import AsyncResult
from fastapi import APIRouter

from api.schemas import Task, TaskData, TaskID
from api.tasks import some_complex_task

router = APIRouter()


@router.get("/tasks/{task_id}")
def get_task_status(task_id: str) -> Task:
  """Return status and result of the celery task."""
  task: AsyncResult[float | None] = AsyncResult(task_id)
  result = None if isinstance(task.result, BaseException) else task.result
  return Task(id=task.id, status=task.status, result=result)


@router.post("/tasks/run")
def run_task(data: TaskData) -> TaskID:
  """Run a background task to be executed in a separate worker process."""
  task = some_complex_task.delay(data.a, data.b)
  return TaskID(id=task.id)
