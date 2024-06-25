import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src'))) # noqa
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))) # noqa

from sqlalchemy import select
from starlette.templating import Jinja2Templates

from src.constants import default_genres

os.makedirs("static", exist_ok=True) # noqa
os.makedirs("images", exist_ok=True) # noqa

import asyncio
from typing import AsyncGenerator, Dict, Any

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from src.models import get_async_session, Base, Movie, Genre
from src.main import app

# DATABASE
DATABASE_URL_TEST = "sqlite+aiosqlite:///./test.db"

engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
Base.metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        async with async_session_maker() as session:
            result = await session.execute(select(Genre))
            genres = result.scalars().all()
            if not genres:
                for genre_name in default_genres:
                    genre = Genre(name=genre_name)
                    session.add(genre)
                await session.commit()
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='session', autouse=True)
def setup_static_dirs():
    # Удаляем фиктивные директории после завершения тестов
    yield
    os.rmdir("static")
    os.rmdir("images")


client = TestClient(app)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def create_movie() -> Dict[str, Any]:
    async with async_session_maker() as session:
        print(await session.execute(select(Genre)))
        movie = Movie(title="Test Movie", producer="Test Producer", year=2022, genre_id=1,
                      description="Test Description")
        session.add(movie)
        await session.commit()
        await session.refresh(movie)

        movie_json = {
            "id": movie.id,
            "title": movie.title,
            "producer": movie.producer,
            "year": movie.year,
            "genre_id": movie.genre_id,
            "description": movie.description
        }

        yield movie_json

        # Cleanup code (если нужно)
        await session.delete(movie)
        await session.commit()
