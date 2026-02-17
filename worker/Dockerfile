FROM ghcr.io/astral-sh/uv:python3.12-alpine

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_NO_DEV=1 \
    UV_PYTHON_DOWNLOADS=0 \
    PATH="/worker/.venv/bin:$PATH"

WORKDIR /worker

COPY ./pyproject.toml ./uv.lock ./run.sh ./

RUN uv sync --locked && chmod +x ./run.sh

COPY ./ ./

CMD ["./run.sh"]
