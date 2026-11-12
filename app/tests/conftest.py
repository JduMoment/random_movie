import pytest

from app.models import TMDB


@pytest.fixture()
def attr_val_map():
    return {
        "id": 1,
        "title": "some title",
        "release_date": "2025-01-01",
        "genre_ids": [2, 3, 4],
        "overview": "some overview",
        "poster_path": "/path/to/poster.jpg",
        "popularity": 1,
        "vote_average": 1,
        "vote_count": 1,
    }


@pytest.fixture
def mock_genres_name_id_map_response(monkeypatch):
    monkeypatch.setattr(TMDB, "genres_name_id_map", {"action": 2, "drama": 3, "triller": 4})
    yield
