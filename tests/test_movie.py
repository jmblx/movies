import pytest
from httpx import AsyncClient
from sqlalchemy import select

from models import Movie
from tests.conftest import async_session_maker


class TestMovie:

    @pytest.mark.asyncio
    async def test_creating_movie(self, ac: AsyncClient):
        try:
            response = await ac.post(
                "/movie",
                json={
                    "title": "string",
                    "producer": "string",
                    "year": 2006,
                    "genre_id": 1,
                    "description": "string"
                },
            )
            print(response.text)
            assert response.status_code == 200
            movie_id = response.json()["id"]
            assert type(movie_id) == int

            async with async_session_maker() as session:
                movie = (await session.execute(select(Movie).where(Movie.id == movie_id))).scalar()
                assert movie.title == "string"
                assert movie.producer == "string"
                assert movie.year == 2006
                assert movie.genre_id == 1
                assert movie.description == "string"
        except Exception as e:
            print(f"Exception occurred: {e}")
            raise e

    # async def test_getting_movie(self, ac: AsyncClient):
    #     response = await ac.get("/movie/1")
    #     assert response.status_code == 200
    #     assert response.json() == {
    #         "id": 1,
    #         "title": "string",
    #         "producer": "string",
