from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers.home import router as home_router

app = FastAPI(
    title="DocuMind",
    version="0.1.0",
    description="Enterprise Document Intelligence Platform",
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(home_router)