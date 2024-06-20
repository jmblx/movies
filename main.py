from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from movie.router import router as router_movie
from pages.router import router as router_pages

from models import init_db

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_db()


app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/images", StaticFiles(directory="images"), name="images")

app.include_router(router_pages)
app.include_router(router_movie)
