from fastapi import FastAPI, status  # noqa: I001

from api.routes import router


app = FastAPI()
app.include_router(router)


@app.get(
  "/health",
  description="Healthcheck of the API",
  responses={
    status.HTTP_200_OK: {
      "description": "Healthcheck status",
      "content": {
        "application/json": {
          "example": {"response": "ok"}
        }
      }
    }
  }
)
async def health() -> dict[str, str]:
  """Healthcheck endpoint."""
  return {"response": "ok"}
