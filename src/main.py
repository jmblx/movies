import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from movie.router import router as router_movie
from pages.router import router as router_pages

from models import init_db



#
# @app.on_event("startup")
# async def on_startup():
#     await init_db()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/images", StaticFiles(directory="images"), name="images")

app.include_router(router_pages)
app.include_router(router_movie)
