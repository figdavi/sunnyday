FROM python:3.13-slim-bookworm

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # Poetry's configuration:
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local' \
  POETRY_VERSION=2.0.0

RUN apt-get update \
  && apt-get install -y curl build-essential gcc \
  && curl -sSL https://install.python-poetry.org | python3 - \
  && apt-get purge --auto-remove -y curl \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /code
COPY poetry.lock pyproject.toml /code/

RUN poetry install --no-interaction --no-ansi

COPY . .

EXPOSE 8000

CMD ["uvicorn", "src.sunnyday.main:app", "--host", "0.0.0.0", "--port", "8000"]