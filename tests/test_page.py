from bs4 import BeautifulSoup
import pytest
from httpx import AsyncClient

from constants import default_genres


class TestPage:

    @pytest.mark.asyncio
    async def test_get_movie(self, ac: AsyncClient, create_movie):
        movie_json = create_movie
        movie_id = movie_json.pop("id")

        response = await ac.get(f"/pages/details/{movie_id}")

        assert response.status_code == 200
        page = response.text
        soup = BeautifulSoup(page, 'lxml')
        details = soup.find('div', class_='movie-details')

        # Проверка наличия всех данных фильма в шаблоне
        genre_id = movie_json.pop("genre_id")
        movie_json["genre"] = default_genres[genre_id - 1]

        try:
            for key, value in movie_json.items():
                assert str(value) in details.text, f"Value '{value}' not found in the details for key '{key}'"
        except AssertionError as e:
            print(f"Ошибка с ключом {key}: {e}")
            raise e
