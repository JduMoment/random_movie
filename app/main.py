from fastapi import FastAPI
from blueprints import routers

app = FastAPI()
app.include_router(routers.router, prefix="")

#
# @app.get("/")
# async def read_root():
#     url = f'{TMDB_BASE_URL}/movie/popular'
#     params = {
#         'api_key': TMDB_API_KEY,
#         'language': 'ru-RU',  # или 'en-US'
#         'page': 1
#     }
#     films = []
#     async with httpx.AsyncClient() as client:
#         response = await client.get(url, params=params)
#         if response.status_code == 200:
#             data = response.json()
#             for movie in data['results']:
#                 films.append(f"{movie['title']} ({movie['release_date']}) — Рейтинг: {movie['vote_average']}")
#         else:
#             print(f"Ошибка: {response.status_code}, {response.text}")
#
#     return '<br>'.join(films)