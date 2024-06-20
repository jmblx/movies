from pydantic import BaseModel
from datetime import datetime


class GenreGet(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class MovieBase(BaseModel):
    title: str
    producer: str
    year: int
    genre_id: int
    description: str


class MovieGet(MovieBase):
    id: int
    pathfile: str
    date_added: datetime
    genre: GenreGet

    class Config:
        from_attributes = True


class MovieAdd(MovieBase):
    pass
