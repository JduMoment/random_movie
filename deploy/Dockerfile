FROM python:3.12-slim

RUN pip install --upgrade pip && pip install poetry

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    PATH="/root/.local/bin:$PATH"

COPY pyproject.toml poetry.lock /tmp/deps/

WORKDIR /tmp/deps
RUN poetry install --no-root
