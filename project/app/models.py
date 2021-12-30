from typing import Optional

from sqlmodel import SQLModel, Field


class MovieBase(SQLModel):
    """pydantic model"""
    title: str
    year: Optional[int] = None
    description: Optional[str] = None


class Movie(MovieBase, table=True):
    """movie db model"""
    id: int = Field(default=None, primary_key=True)


class MovieCreate(MovieBase):
    """pydantic create model"""
    pass
