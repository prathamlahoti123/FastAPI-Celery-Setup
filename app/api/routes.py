from celery.result import AsyncResult
from fastapi import APIRouter

from api.schemas import Task, TaskData, TaskID
from api.tasks import some_complex_task

router = APIRouter()


@router.get("/tasks/{task_id}")
def get_task_status(task_id: str) -> Task:
  """Return status and result of the celery task."""
  res = AsyncResult(task_id)
  return Task(id=res.id, status=res.status, result=res.result)


@router.post("/tasks/run")
def run_task(data: TaskData) -> TaskID:
  """Run a background task to be executed in a separate worker process."""
  task: AsyncResult = some_complex_task.delay(data.a, data.b)
  return TaskID(id=task.id)
