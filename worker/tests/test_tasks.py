from typing import TYPE_CHECKING
from uuid import UUID

import pytest

from app.tasks import div, some_complex_task
from tests.conftest import E2E_MODE_DISABLED

if TYPE_CHECKING:
  from celery.result import AsyncResult


def test_div() -> None:
  """Test for app.tasks.div function."""
  assert div(2, 2) == 1.0


def test_run_task() -> None:
  """Test sending a task to the celery queue."""
  res: AsyncResult = some_complex_task.delay(2, 2)
  assert res.result is None
  assert res.status == "PENDING"
  try:
    UUID(res.id)
  except ValueError:
    pytest.fail("Task ID is not a valid UUID")


@pytest.mark.skipif(E2E_MODE_DISABLED, reason="E2E mode disabled")
def test_e2e_run_task() -> None:
  """E2E test to run the task with a real broker and worker."""
