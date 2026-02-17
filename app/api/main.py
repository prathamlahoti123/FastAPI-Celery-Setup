from fastapi import FastAPI, Response, status

from api.routes import router
from api.settings import settings

app = FastAPI(**settings.fastapi_kwargs)
app.include_router(router)


@app.get("/health", status_code=status.HTTP_204_NO_CONTENT)
async def health() -> Response:
  """Return health status of the API."""
  return Response(
    status_code=status.HTTP_204_NO_CONTENT,
    headers={"x-status": "health"},
  )
