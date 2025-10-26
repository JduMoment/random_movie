from fastapi import APIRouter
from views import main_page_view

router = APIRouter()

router.add_api_route("/", endpoint=main_page_view.get, methods=["GET"])
router.add_api_route("/", endpoint=main_page_view.post, methods=["POST"])
