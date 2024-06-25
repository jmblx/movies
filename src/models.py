import uuid
from datetime import datetime
from typing import AsyncGenerator, Annotated

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base, mapped_column, Mapped, relationship
from sqlalchemy import Integer, String, DateTime, text, ForeignKey, select

from constants import default_genres

DATABASE_URL = "sqlite+aiosqlite:///./test.db"


engine = create_async_engine(DATABASE_URL, echo=True)


async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
added_at = Annotated[
    datetime,
    mapped_column(
        nullable=True, server_default=text("TIMEZONE('utc', now())")
    ),
]
Base = declarative_base()


class Movie(Base):
    __tablename__ = 'movies'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    producer: Mapped[str] = mapped_column(String, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    genre_id: Mapped[int] = mapped_column(ForeignKey("genres.id"), nullable=False)
    genre: Mapped["Genre"] = relationship("Genre", back_populates="movies")
    description: Mapped[str] = mapped_column(String)
    pathfile: Mapped[str] = mapped_column(String, default=f"{uuid.uuid4()}")
    date_added: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Genre(Base):
    __tablename__ = 'genres'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    movies: Mapped[list[Movie]] = relationship("Movie", order_by=Movie.id, back_populates="genre")


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_maker() as session:
        result = await session.execute(select(Genre))
        genres = result.scalars().all()
        if not genres:
            for genre_name in default_genres:
                genre = Genre(name=genre_name)
                session.add(genre)
            await session.commit()
