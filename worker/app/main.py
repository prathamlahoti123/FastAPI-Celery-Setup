
from celery import Celery  # noqa: I001

from app.settings import settings


celery = Celery(
  __name__,
  broker=settings.celery_broker_url,
  backend=settings.celery_result_backend,
  include=["app.tasks"],
)
