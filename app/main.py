from fastapi import FastAPI
from blueprints import routers
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
app.include_router(routers.router, prefix="")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(SessionMiddleware, secret_key="super-secret-key-123")
