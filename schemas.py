from __future__ import annotations
import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class BookBase(BaseModel):
    title: str = Field(..., max_length=255)
    summary: Optional[str] = None
    publication_date: Optional[datetime.date] = None


class BookCreate(BookBase):
    author_id: int


class BookUpdate(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = None
    publication_date: Optional[datetime.date] = None
    author_id: Optional[int] = None


class AuthorSimple(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class BookRead(BookBase):
    id: int
    author: Optional[AuthorSimple] = None

    class Config:
        orm_mode = True


class AuthorBase(BaseModel):
    name: str = Field(..., max_length=255)
    bio: Optional[str] = None


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(BaseModel):
    name: Optional[str] = None
    bio: Optional[str] = None


class AuthorRead(AuthorBase):
    id: int
    books: List[BookRead] = []

    class Config:
        orm_mode = True

