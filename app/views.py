from dependencies import templates
from starlette.responses import RedirectResponse
from typing import TYPE_CHECKING
from models import TMDB, FlashMessages
import json
from fastapi import Request


class MainPageView:
    async def get(self, request: Request):
        tmbd = TMDB()
        flash = FlashMessages(request=request)
        filter_data_map = (
            json.loads(fdm) if (fdm := request.session["filter_data_map"]) else {}
        )
        movie = await tmbd.get_random_movie(request, filter_data_map.copy())
        return templates.TemplateResponse(
            "base.html",
            {
                "request": request,
                "movie": movie,
                "selected_filters": filter_data_map,
                "flash_messages": flash.flash_messages,
            },
        )

    async def post(self, request: Request):
        post_form = await request.form()
        filter_data_map = {
            filter_name: (
                post_form.getlist(filter_name) if filter_name == "genre" else val
            )
            for filter_name, val in post_form.items()
            if val
        }
        request.session["filter_data_map"] = json.dumps(filter_data_map)
        return RedirectResponse(request.url_for("get"), status_code=303)


main_page_view = MainPageView()
