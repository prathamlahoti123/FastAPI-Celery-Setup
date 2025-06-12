FROM python:3.12-alpine3.19
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8
WORKDIR /worker
COPY ./worker/requirements.txt ./
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r ./requirements.txt
CMD ["celery", "-A", "app.main", "worker", "-l", "INFO"]
