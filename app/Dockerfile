FROM python:3.12-alpine3.19
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8
WORKDIR /api
COPY ./app/requirements.txt ./
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r ./requirements.txt
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
