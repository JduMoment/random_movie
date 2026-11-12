from pydantic import BaseModel, Field
import os
from functools import cached_property
from typing import TYPE_CHECKING, Self
import httpx
import random

if TYPE_CHECKING:
    from fastapi import Request


class Movie(BaseModel):
    id: int = Field(..., alias="movie_id")
    title: str = Field(..., min_length=1)
    release_date: str = Field(..., min_length=10, max_length=10)
    genre_ids: list = Field(..., min_length=1)
    overview: str | None = None
    poster_path: str | None = None
    popularity: float = 0
    vote_average: float | None = None
    vote_count: int = 0

    @classmethod
    def create(cls, **kwargs) -> Self | None:
        """
        Фабричный метод для валидации на этапе создания.
        """
        movie = None

        if cls.is_valid_movie(**kwargs):
            movie = cls(
                movie_id=kwargs["id"],
                title=kwargs["title"],
                release_date=kwargs["release_date"],
                genre_ids=kwargs["genre_ids"],
                overview=kwargs["overview"],
                poster_path=kwargs["poster_path"],
                popularity=kwargs.get("popularity", 0),
                vote_average=kwargs.get("vote_average", None),
                vote_count=kwargs.get("vote_count", 0),
            )
        return movie

    @classmethod
    def is_valid_movie(cls, **kwargs) -> bool:
        required_fields = ("id", "title", "release_date", "genre_ids", "overview", "poster_path")
        return all(kwargs.get(field) for field in required_fields)

    @property
    def release_date_display(self) -> str:
        return ".".join(self.release_date.split("-")[::-1])

    @property
    def genres(self) -> list:
        genres_id_name_map = {
            genre_id: genre_name
            for genre_name, genre_id in TMDB().genres_name_id_map.items()
        }
        return [genres_id_name_map[genre_id] for genre_id in self.genre_ids if genre_id in genres_id_name_map]


class TMDB:
    async def get_movies(self, filter_data_map: dict | None = None) -> dict | None:
        filters = self.filter_kwargs(filter_data_map)

        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{os.getenv('TMDB_BASE_URL')}/discover/movie", params={**filters}
            )

            return resp.json()

    @cached_property
    def genres_name_id_map(self) -> dict | None:
        url = f"{os.getenv('TMDB_BASE_URL')}/genre/movie/list"
        params = {"api_key": os.getenv("TMDB_API_KEY"), "language": "ru-RU"}

        with httpx.Client() as client:
            response = client.get(url=url, params=params)
            data = response.json()
            return {genre["name"]: genre["id"] for genre in data["genres"]}

    def filter_kwargs(self, filter_data_map: dict | None = None) -> dict:
        if not filter_data_map:
            return {}

        if any(
            rating_field in filter_data_map
            for rating_field in ("vote_average.gte", "vote_average.lte")
        ):
            filter_data_map["vote_count.gte"] = 50

        genre_type = filter_data_map.pop("genre_types", "|")

        if genre_type != "without_genres":
            filter_data_map["with_genres"] = genre_type.join(
                str(self.genres_name_id_map.get(genre_name))
                for genre_name in filter_data_map.pop("genre", [])
            )
        else:
            filter_data_map[genre_type] = ",".join(
                str(self.genres_name_id_map.get(genre_name))
                for genre_name in filter_data_map.pop("genre", [])
            )

        filter_data_map["api_key"] = os.getenv("TMDB_API_KEY")
        filter_data_map["language"] = "ru-RU"
        filter_data_map["certification_country"] = "RU"

        return filter_data_map

    async def get_random_movie(
        self, request: "Request", filter_data_map: dict | None = None
    ) -> Movie | None:
        movies = await self.get_movies(filter_data_map) or {}
        results = list(movies.get("results") or [])
        random.shuffle(results)

        for random_movie in results:
            if movie := Movie.create(**random_movie):
                return movie

        flash = FlashMessages(request=request)
        flash.add_flash(
            "Не удалось найти фильмов, подходящих под выбранные фильтры. Измените фильтрацию.",
            "warning",
        )
        return None


class FlashMessages:
    def __init__(self, request: "Request"):
        self.FLASH_SESSION_KEY = "_flashes"
        self.request = request

    def add_flash(self, message: str, category: str) -> None:
        if self.FLASH_SESSION_KEY not in self.request.session:
            self.request.session[self.FLASH_SESSION_KEY] = []
        self.request.session[self.FLASH_SESSION_KEY].append(
            {"message": message, "category": category}
        )

    @property
    def flash_messages(self) -> list[dict[str, str]]:
        flash_messages = self.request.session.pop(self.FLASH_SESSION_KEY, [])
        return flash_messages
