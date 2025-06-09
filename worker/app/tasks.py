from typing import TYPE_CHECKING

from app.main import celery

if TYPE_CHECKING:
  from celery.app.task import Task


def div(a: int, b: int) -> float:
  """Perform division of 2 numbers and return the result.

  NOTE: this function contains some business logic to be
        executed within a background task.
  """
  return a / b


@celery.task(
  name="some-complex-task",
  bind=True,
  max_retries=2,
  default_retry_delay=5,
)
def some_complex_task(self: "Task", a: int, b: int) -> float:
  """Run a 'CPU-intensive' math operation in the background task.

  NOTE (1): the business logic and the actual task are separated
            in order to test them as different units.

  NOTE (2): retry policy is strictly used for demonstration purposes.
  """
  try:
    res = div(a, b)
  except ZeroDivisionError as exc:
    raise self.retry(exc=exc)  # noqa: B904
  return res
