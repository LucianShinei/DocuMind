from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
    request,
    "index.html",
    {
        "title": "Home",
        "active_page": "home",
    },
)


@router.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse(
    request,
    "about.html",
    {
        "title": "About",
        "active_page": "about",
    },
    )