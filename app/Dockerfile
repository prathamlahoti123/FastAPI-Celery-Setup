FROM ghcr.io/astral-sh/uv:python3.12-alpine

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_NO_DEV=1 \
    UV_PYTHON_DOWNLOADS=0 \
    PATH="/api/.venv/bin:$PATH"

WORKDIR /api

COPY ./pyproject.toml ./uv.lock ./

RUN uv sync --locked

COPY ./ ./

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
