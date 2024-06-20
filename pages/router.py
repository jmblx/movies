# routers.py
from typing import List

from fastapi import APIRouter, Request, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from starlette.templating import Jinja2Templates

from models import get_async_session, Movie, Genre
from movie.schemas import MovieGet

router = APIRouter(prefix="/pages")

templates = Jinja2Templates(directory="templates")


@router.get("/add")
async def add_page(request: Request, session: AsyncSession = Depends(get_async_session)):
    genres = await session.execute(select(Genre))
    genres_list = genres.scalars().all()
    return templates.TemplateResponse(
        request=request, name="add.html", context={"request": request, "genres": genres_list}
    )


@router.get("/catalog")
async def catalog_page(request: Request, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Movie).options(joinedload(Movie.genre)))
    movies = result.scalars().all()
    movies_list: List[MovieGet] = [MovieGet.model_validate(movie) for movie in movies]
    return templates.TemplateResponse(
        "catalog.html",
        {"request": request, "movies": movies_list}
    )


@router.get("/details/{movie_id}")
async def details_page(request: Request, movie_id: int, session: AsyncSession = Depends(get_async_session)):
    movie = await session.execute(select(Movie).where(Movie.id == movie_id).options(joinedload(Movie.genre)))
    movie = MovieGet.model_validate(movie.scalar())
    return templates.TemplateResponse(
        request=request, name="details.html", context={"movie": movie}
    )
