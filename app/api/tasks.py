from celery import shared_task


@shared_task(name="some-complex-task")
def some_complex_task(*args: int, **kwargs: int) -> None:
  """'CPU-intensive' task to be processed by Celery worker.

  Optional number of retries and delay between retries
  can be passed as keyword arguments. For example:
    task = some_complex_task.delay(data.a, data.b, retry_attempts=6, retry_delay=10)

  If not passed, default values defined by the worker will be used.
  """
