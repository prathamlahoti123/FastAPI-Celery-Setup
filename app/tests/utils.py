from typing import TYPE_CHECKING

from httpx import codes

from api.schemas import Task

if TYPE_CHECKING:
  from httpx import Client


def get_task_info(client: "Client", task_id: str) -> Task:
  """Return info about task with given ID."""
  res = client.get(f"/tasks/{task_id}")
  assert res.status_code == codes.OK
  return Task(**res.json())
