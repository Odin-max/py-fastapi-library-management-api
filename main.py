from fastapi import FastAPI, Depends, HTTPException, status
from typing import List, Optional
from database import engine, Base, get_db

import crud, schemas

app = FastAPI(title="Library Management API")


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.post("/authors", response_model=schemas.AuthorRead, status_code=status.HTTP_201_CREATED)
def create_author(author: schemas.AuthorCreate, db=Depends(get_db)):
    existing = crud.get_author_by_name(db, author.name)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Author already exists")
    return crud.create_author(db, author)


@app.get("/authors", response_model=List[schemas.AuthorRead])
def list_authors(skip: int = 0, limit: int = 100, db=Depends(get_db)):
    return crud.get_authors(db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.AuthorRead)
def get_author(author_id: int, db=Depends(get_db)):
    db_author = crud.get_author(db, author_id)
    if not db_author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
    return db_author


@app.post("/authors/{author_id}/books", response_model=schemas.BookRead, status_code=status.HTTP_201_CREATED)
def create_book_for_author(author_id: int, book: schemas.BookCreate, db=Depends(get_db)):
    db_author = crud.get_author(db, author_id)
    if not db_author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")

    book_data = book.dict()
    book_data["author_id"] = author_id
    book_obj = schemas.BookCreate(**book_data)
    return crud.create_book(db, book_obj)


@app.get("/books", response_model=List[schemas.BookRead])
def list_books(skip: int = 0, limit: int = 100, author_id: Optional[int] = None, db=Depends(get_db)):
    # use CRUD layer to list/filter books
    return crud.get_books(db, skip=skip, limit=limit, author_id=author_id)