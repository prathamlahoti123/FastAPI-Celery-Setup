import os  # noqa: I001
from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from api.main import app


# e2e mode should be enabled when running e2e tests
E2E_MODE_DISABLED = bool(int(os.getenv("E2E_MODE_ENABLED", "1")))
if E2E_MODE_DISABLED:
  os.environ["CELERY_BROKER_URL"] = "memory://"
  os.environ["CELERY_RESULT_BACKEND"] = "rpc://"


@pytest.fixture(scope="session")
def client() -> Iterator[TestClient]:
  """HTTP client to test FastAPI endpoints."""
  with TestClient(app) as cl:
    yield cl
