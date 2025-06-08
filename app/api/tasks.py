from celery import shared_task


@shared_task(name="some-complex-task")
def some_complex_task(*args: int, **kwargs: int) -> None:
  """'CPU-intensive' task to be processed by Celery worker."""
