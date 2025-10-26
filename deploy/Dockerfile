FROM python:3.12-slim

RUN pip install --upgrade pip && pip install poetry

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    PATH="/root/.local/bin:$PATH"

COPY pyproject.toml /tmp/deps/

WORKDIR /tmp/deps
RUN poetry lock && poetry install --no-root

#Запускать из директории random_movie командой: docker build -f deploy/Dockerfile -t random_movie .