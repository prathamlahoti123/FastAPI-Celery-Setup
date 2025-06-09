import os  # noqa: I001


# e2e mode should be enabled when running e2e tests
E2E_MODE_DISABLED = bool(int(os.getenv("E2E_MODE_ENABLED", "1")))
if E2E_MODE_DISABLED:
  os.environ["CELERY_BROKER_URL"] = "memory://"
  os.environ["CELERY_RESULT_BACKEND"] = "rpc://"
