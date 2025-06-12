import os
import time
from typing import TYPE_CHECKING

import pytest
from fastapi import status

from api.schemas import TaskData
from api.tasks import some_complex_task

if TYPE_CHECKING:
  from celery.result import AsyncResult
  from fastapi.testclient import TestClient
  from httpx import Client


# End-to-end mode should be enabled when running end-to-end tests
E2E_MODE_DISABLED = bool(int(os.getenv("E2E_MODE_DISABLED", "1")))


def test_health(client: "TestClient") -> None:
  """Test healthcheck endpoint."""
  resp = client.get("/health")
  assert resp.status_code == status.HTTP_200_OK
  assert resp.json() == {"response": "ok"}


@pytest.mark.parametrize(
  "task_data",
  [TaskData(a=2, b=2)]
)
def test_run_task(task_data: TaskData) -> None:
  """Test sending a task to the celery queue."""
  os.environ["CELERY_BROKER_URL"] = "memory://"
  os.environ["CELERY_RESULT_BACKEND"] = "rpc://"

  res: AsyncResult = some_complex_task.delay(task_data.a, task_data.b)
  assert res.result is None
  assert res.status == "PENDING"
  assert res.id


@pytest.mark.parametrize(
  ("task_data", "result"),
  [
    (TaskData(a=2, b=2), 1.0),
    (TaskData(a=4, b=2), 2.0)
  ]
)
@pytest.mark.skipif(E2E_MODE_DISABLED, reason="E2E mode disabled")
def test_e2e_run_task(e2e_client: "Client", task_data: TaskData, result: float) -> None:
  """E2E test to run the task with a real broker and worker."""
  run_task_res = e2e_client.post(
    "/tasks/run",
    json=task_data.model_dump()
  )
  assert run_task_res.status_code == status.HTTP_200_OK
  assert "id" in run_task_res.json()
  task_id = run_task_res.json()["id"]

  # Add delay to make sure the task is finished
  time.sleep(0.5)

  # Get info about task
  get_task_res = e2e_client.get(f"/tasks/{task_id}")
  assert get_task_res.status_code == status.HTTP_200_OK
  task_info = get_task_res.json()
  assert task_info["id"] == task_id
  assert task_info["status"] == "SUCCESS"
  assert task_info["result"] == result


@pytest.mark.parametrize(
  "task_data",
  [TaskData(a=2, b=0)]
)
@pytest.mark.skipif(E2E_MODE_DISABLED, reason="E2E mode disabled")
def test_e2e_run_task_with_error(e2e_client: "Client", task_data: TaskData) -> None:
  """E2E test to run the task with a real broker and worker."""
  run_task_res = e2e_client.post(
    "/tasks/run",
    json=task_data.model_dump()
  )
  assert run_task_res.status_code == status.HTTP_200_OK
  assert "id" in run_task_res.json()
  task_id = run_task_res.json()["id"]

  # Get info about task
  get_task_res = e2e_client.get(f"/tasks/{task_id}")
  assert get_task_res.status_code == status.HTTP_200_OK
  task_info = get_task_res.json()
  assert task_info["id"] == task_id
  assert task_info["status"] == "RETRY"
  assert task_info["result"] is None
