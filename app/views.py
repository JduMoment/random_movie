from dependencies import templates
from starlette.responses import RedirectResponse
from models import TMDB, FlashMessages
import json
from datetime import date
from fastapi import Request


class MainPageView:
    async def get(self, request: Request):
        tmdb = TMDB()
        flash = FlashMessages(request=request)
        filter_data_map = (
            json.loads(fdm) if (fdm := request.session.get("filter_data_map")) else {}
        )
        movie = await tmdb.get_random_movie(request, filter_data_map.copy())
        today = date.today()
        return templates.TemplateResponse(
            "base.html",
            {
                "request": request,
                "movie": movie,
                "selected_filters": filter_data_map,
                "release_date_max": f"{today.year}-12-31",
                "release_date_gte_default": today.replace(year=today.year - 1, day=min(today.day, 28)).isoformat(),
                "release_date_lte_default": today.isoformat(),
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
