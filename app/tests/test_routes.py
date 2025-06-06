from typing import TYPE_CHECKING

import pytest
from fastapi import status

if TYPE_CHECKING:
  from httpx import AsyncClient


@pytest.mark.anyio
async def test_health(client: "AsyncClient") -> None:
  """Test healthcheck endpoint."""
  resp = await client.get("/health")
  assert resp.status_code == status.HTTP_200_OK
  assert resp.json() == {"response": "ok"}
