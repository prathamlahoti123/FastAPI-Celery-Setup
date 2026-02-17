from celery import Celery

from app.settings import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

celery = Celery(
  __name__,
  broker=CELERY_BROKER_URL,
  backend=CELERY_RESULT_BACKEND,
  include=["app.tasks"],
)
