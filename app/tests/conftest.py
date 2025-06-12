from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from httpx import Client

from api.main import app


@pytest.fixture(scope="session")
def client() -> Iterator[TestClient]:
  """HTTP client to test FastAPI endpoints."""
  with TestClient(app) as cl:
    yield cl


@pytest.fixture(scope="session")
def e2e_client() -> Iterator[Client]:
  """HTTP client to test FastAPI endpoints in E2E mode."""
  with Client(base_url="http://localhost:8000") as cl:
    yield cl
