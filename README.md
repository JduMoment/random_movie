# Random Movie 🎬

Пусть великий рандом решит, какой фильм посмотреть сегодня вечером.

Веб-приложение на FastAPI: выбираете фильтры, оно запрашивает подборку фильмов из [TMDB](https://www.themoviedb.org/) и показывает один случайный фильм с постером, описанием, жанрами и рейтингом.

## Возможности

- Случайный фильм из TMDB Discover API
- Фильтры:
  - жанры: исключить выбранные, совпадение всех или хотя бы одного
  - диапазон дат выхода
  - диапазон рейтинга (учитываются только фильмы с 50+ голосами)
  - язык оригинала
  - возрастное ограничение (RU)
- Фильтры хранятся в сессии, после перезагрузки страницы выпадает новый фильм с теми же настройками
- Flash-сообщение, если под фильтры ничего не нашлось

## Стек

Python 3.11+, FastAPI, Jinja2, httpx, Pydantic, Poetry, Docker.

## Структура

```
app/
├── main.py              # создание приложения FastAPI, статика, сессии
├── blueprints/routers.py# маршруты (GET / и POST /)
├── views.py             # обработчики главной страницы
├── models.py            # Movie, клиент TMDB, FlashMessages
├── dependencies.py      # Jinja2-шаблоны, загрузка .env
├── templates/           # HTML-шаблоны
├── static/              # CSS и JS
└── tests/               # pytest
deploy/
├── Dockerfile
└── docker-compose.yml
```

## Настройка

Создайте файл `app/.env`:

```env
TMDB_API_KEY=ваш_ключ_tmdb
TMDB_BASE_URL=https://api.themoviedb.org/3
SECRET_KEY=случайная_строка_для_подписи_сессий
```

API-ключ выдаётся бесплатно в [настройках аккаунта TMDB](https://www.themoviedb.org/settings/api).

## Запуск локально

```bash
poetry install
cd app
poetry run uvicorn main:app --reload
```

Приложение будет доступно на http://localhost:8000.

> Запускайте именно из папки `app/`: импорты и пути к `templates/` и `static/` считаются от неё.

## Запуск в Docker

```bash
cd deploy
docker compose up --build
```

Папка `app/` монтируется в контейнер, так что изменения в коде подхватываются без пересборки.

Собрать образ отдельно (из корня репозитория):

```bash
docker build -f deploy/Dockerfile -t random_movie .
docker run -p 8000:8000 --env-file app/.env random_movie
```

## Тесты и линтер

```bash
poetry run pytest app --cov=app
poetry run ruff check .
poetry run ruff format .
```

## Лицензия

MIT
