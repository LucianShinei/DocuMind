from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers.home import router as home_router
from app.config.settings import settings

from contextlib import asynccontextmanager

from app.database.mongodb import (
    connect_to_mongo,
    close_mongo_connection,
)

from app.routers.documents import router as document_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()

    yield

    await close_mongo_connection()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    lifespan=lifespan,
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(home_router)
app.include_router(document_router)