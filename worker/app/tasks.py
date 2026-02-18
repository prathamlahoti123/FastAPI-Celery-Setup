from typing import TYPE_CHECKING

from app.main import celery
from app.settings import CELERY_MAX_RETRIES, CELERY_RETRY_DELAY

if TYPE_CHECKING:
  from celery.app.task import Task


def div(a: int, b: int) -> float:
  """Perform division of 2 numbers and return the result.

  NOTE: this function contains some business logic to be
        executed within a background task.
  """
  return a / b


@celery.task(name="some-complex-task", bind=True)
def some_complex_task(
  self: "Task[..., float]",
  /,
  a: int,
  b: int,
  **kwargs: int,
) -> float:
  """Run the task with given input arguments on the background."""
  try:
    res = div(a, b)
  except ZeroDivisionError as exc:
    raise self.retry(
      exc=exc,
      max_retries=kwargs.get("retry_attempts", CELERY_MAX_RETRIES),
      countdown=kwargs.get("retry_delay", CELERY_RETRY_DELAY),
    ) from exc
  return res
