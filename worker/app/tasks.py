import time

from celery.utils.log import get_task_logger

from app.main import celery


logger = get_task_logger(__name__)


@celery.task(
  name="some-complex-task",
  bind=True,
  max_retries=2,
  default_retry_delay=10,
)
def some_complex_task(self, a: int, b: int) -> float | None:
  """'CPU-intensive' task to calculate a complex math operation"""
  logger.info("Running the background task ...")
  try:
    res = a / b
  except ZeroDivisionError as exc:
    logger.error(str(exc))
    self.retry(exc=exc)
  # simulate processing ...
  time.sleep(10)
  return res
