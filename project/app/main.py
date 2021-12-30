from typing import Any, List

from fastapi import Depends, FastAPI
from structlog import get_logger
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.models import Movie, MovieCreate

app = FastAPI()
logger = get_logger(__name__)


@app.get("/health")
async def health_check() -> Any:
    """health check route"""
    logger.debug("health_check")
    return {"status": "healthy"}


@app.get("/movies", response_model=list[Movie])
async def get_movies(
    session: AsyncSession = Depends(get_session)
) -> List[Movie]:
    """get a list of movies"""
    logger.debug("get_movies")

    result = await session.execute(select(Movie))
    movies = result.scalars().all()
    return [Movie(
        title=movie.title,
        year=movie.year,
        description=movie.description,
        id=movie.id
    ) for movie in movies]


@app.post("/movies")
async def add_movie(
    movie: MovieCreate,
    session: AsyncSession = Depends(get_session)
) -> Movie:
    """create a movie"""
    logger.debug("add_movie")

    movie = Movie(
        title=movie.title,
        year=movie.year,
        description=movie.description
    )
    session.add(movie)
    await session.commit()
    await session.refresh(movie)
    return movie
