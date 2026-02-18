import os
import time
from typing import TYPE_CHECKING

import pytest
from celery import states
from fastapi import status

from api.schemas import TaskData
from api.tasks import some_complex_task

from .utils import get_task_info

if TYPE_CHECKING:
  from fastapi.testclient import TestClient
  from httpx import Client


def test_health(client: "TestClient") -> None:
  """Test healthcheck endpoint."""
  resp = client.get("/health")
  assert resp.status_code == status.HTTP_204_NO_CONTENT
  assert resp.headers.get("x-status") == "health"


@pytest.mark.parametrize("task_data", [TaskData(a=2, b=2)])
def test_run_task(task_data: TaskData) -> None:
  """Test sending a task to the celery queue."""
  os.environ["CELERY_BROKER_URL"] = "memory://"
  os.environ["CELERY_RESULT_BACKEND"] = "rpc://"

  res = some_complex_task.delay(task_data.a, task_data.b)
  assert res.result is None
  assert res.status == states.PENDING
  assert res.id


@pytest.mark.parametrize(
  ("task_data", "result"),
  [(TaskData(a=2, b=2), 1.0), (TaskData(a=4, b=2), 2.0)],
)
@pytest.mark.e2e
def test_e2e_run_task(e2e_client: "Client", task_data: TaskData, result: float) -> None:
  """E2E test to run the task with a real broker and worker."""
  run_task_res = e2e_client.post("/tasks/run", json=task_data.model_dump())
  assert run_task_res.status_code == status.HTTP_200_OK
  task_id = run_task_res.json()["id"]

  # Add delay to make sure the task is finished
  time.sleep(0.5)

  task = get_task_info(e2e_client, task_id)
  assert task.status == states.SUCCESS
  assert task.result == result


@pytest.mark.parametrize("task_data", [TaskData(a=2, b=0)])
@pytest.mark.e2e
def test_e2e_run_task_with_error(e2e_client: "Client", task_data: TaskData) -> None:
  """E2E test to run the task with a real broker and worker."""
  run_task_res = e2e_client.post("/tasks/run", json=task_data.model_dump())
  assert run_task_res.status_code == status.HTTP_200_OK
  task_id = run_task_res.json()["id"]

  # wait until the task changes its state from PENDING to RETRY
  time.sleep(0.5)

  # Check the result of the task with invalid input data
  task = get_task_info(e2e_client, task_id)
  assert task.status == states.RETRY
  assert task.result is None

  # wait until retry attempts are exhausted
  time.sleep(3.5)

  # Make sure the task is failed after retrying
  task = get_task_info(e2e_client, task_id)
  assert task.status == states.FAILURE
  assert task.result is None
