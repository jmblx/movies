import logging
import os
import shutil

from fastapi import APIRouter, Depends, UploadFile, HTTPException
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from models import Movie, get_async_session, async_session_maker
from movie.schemas import MovieAdd
from PIL import Image

router = APIRouter(prefix="/movie")
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)
IMAGES_DIR = os.path.join(PARENT_DIR, "images")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_upload_avatar(
    object_id,
    file,
    class_,
    path: str,
):
    async with async_session_maker() as session:
        object = await session.get(class_, object_id)
        save_path = os.path.join(path, f"object{object.id}{file.filename}")
        file_name = os.path.splitext(save_path)[0] + ".webp"
        with open(save_path, "wb") as new_file:
            shutil.copyfileobj(file.file, new_file)

        with Image.open(save_path) as img:
            img = img.resize((350, 350))
            img.save(file_name, "WEBP")

        os.remove(save_path)

        object.pathfile = f"object{object.id}{file.filename.split('.')[0]}.webp"
        await session.commit()
    return file_name


@router.post("")
async def add_movie(movie: MovieAdd, session: AsyncSession = Depends(get_async_session)):
        # movie = Movie(**movie.model_dump())
    try:
        movie_id = await session.execute(insert(Movie).values(**movie.model_dump()).returning(Movie.id))
        await session.commit()
        return {"id": movie_id.scalar()}
    except Exception as e:
        logger.error(f"Error occurred while creating movie: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# @router.get("/{movie_id}", response_model=MovieGet)
# async def get_movie(movie_id: int, session: AsyncSession = Depends(get_async_session)):
#     movie = await session.get(Movie, movie_id)
#     if not movie:
#         raise HTTPException(status_code=404, detail="Movie not found")
#     return movie


@router.post("/photo/{movie_id}")
async def update_photo(movie_id: int, file: UploadFile):
    class_ = Movie
    res = await create_upload_avatar(movie_id, file, class_, IMAGES_DIR)
    return res
