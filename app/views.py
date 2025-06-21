from fastapi import Request
from fastapi.responses import HTMLResponse
from dependencies import templates

class MainPageView:
    def __init__(self):
        # инициализация, если нужно (например, TMDbClient)
        pass

    async def get(self, request: Request):
        return templates.TemplateResponse("base.html", {"request": request})

    async def post(self, request: Request):
        return HTMLResponse("<h1>POST: Добавить фильм</h1>")

main_page_view = MainPageView()