from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app=FastAPI(
    title="DocuMind",   
    version="0.1.0",
    description="Enterprise Document Intelligence Platform"
)

templates = Jinja2Templates(directory="app/templates")

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "title": "DocuMind",
            "user": "Ansh",
            "version": "0.1.0"
        }
    )


@app.get("/about")
async def about():
    return {
        "project": "DocuMind",
        "version": "0.1.0"
    }