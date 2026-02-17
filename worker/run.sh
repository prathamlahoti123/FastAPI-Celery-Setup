#!/bin/sh

set -e

watchmedo auto-restart --directory=./ \
  --pattern=*.py \
  --recursive \
  -- \
  celery -A app.main worker \
  -l ${CELERY_LOGLEVEL:=INFO}
