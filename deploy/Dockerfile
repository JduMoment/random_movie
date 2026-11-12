FROM python:3.12-slim

RUN pip install --upgrade pip && pip install poetry

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

COPY pyproject.toml poetry.lock /tmp/deps/

WORKDIR /tmp/deps
RUN poetry install --no-root

COPY app /app
WORKDIR /app

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Сборка из корня репозитория: docker build -f deploy/Dockerfile -t random_movie .
