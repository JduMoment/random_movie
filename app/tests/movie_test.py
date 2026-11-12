from app.models import Movie


def test_create_movie(attr_val_map):
    assert Movie.create(**attr_val_map) is not None

    attr_val_map["title"] = None

    assert Movie.create(**attr_val_map) is None

def test_release_date_display(attr_val_map):
    movie = Movie.create(**attr_val_map)
    movie_rel_date_display = "01.01.2025"

    assert movie.release_date_display == movie_rel_date_display

def test_genres(attr_val_map, mock_genres_name_id_map_response):
    movie = Movie.create(**attr_val_map)

    assert movie.genres == ["action", "drama", "triller"]
