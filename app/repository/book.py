from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from app.models.book import Book
from app.models.genre import Genre
from app.models.author import Author
from app.models.user_book_ratings import UserBookRating
from app.schemas.pagination import Pagination
from app.schemas.book import BookFilter, SimiliarBookFilter, GetCFSVDRecommendation, AddRating, BookTitleFilter
from typing import Union, Any
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

def get_all_books(book_filter: BookFilter, pagination: Pagination, db: Session):
  query = db.query(Book).options(
    joinedload(Book.genres),
    joinedload(Book.authors)
  ).order_by(Book.score.desc())

  if len(book_filter.language_codes) != 0:
    query = query.filter(Book.language_code.in_(book_filter.language_codes))

  if len(book_filter.genres) != 0:
    query = query.join(Book.genres).filter(Genre.name.in_(book_filter.genres))
    
  if len(book_filter.authors) != 0:
    author_filters = [
      Author.name.ilike(f"%{name}%") 
      for name in book_filter.authors
    ]

    query = query.join(Book.authors).filter(or_(*author_filters))

  books = (
    query
    .offset(pagination.skip)
    .limit(pagination.limit)
    .all()
  )
  total = query.count()

  return books, total

def get_detail_book(id: int, db: Session):
  book = db.query(Book).filter(Book.id == id).first()

  return book

def get_similiar_books(
  book_filter: Union[SimiliarBookFilter, GetCFSVDRecommendation, Any],
  pagination: Pagination,
  ids: list[int],
  db: Session
):
  query = db.query(Book).options(joinedload(Book.genres)).filter(Book.id.in_(ids))

  if isinstance(book_filter, SimiliarBookFilter):
    if len(book_filter.language_codes) != 0:
      query = query.filter(Book.language_code.in_(book_filter.language_codes))

    if len(book_filter.genres) != 0:
      query = query.join(Book.genres).filter(Genre.name.in_(book_filter.genres))

  books = (
    query
    .offset(pagination.skip)
    .limit(pagination.limit)
    .all()
  )
  total = query.count()

  return books, total

def get_book_rating(book_id: int, user_id: int, db: Session):
  book_rating = db.query(UserBookRating).filter_by(user_id=user_id, book_id=book_id).first()
  
  return book_rating

def add_rating(add_rating_data: UserBookRating, db: Session):
  try: 
      db.add(add_rating_data)
      db.commit()
      db.refresh(add_rating_data)
  except IntegrityError as e:
      db.rollback()
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.orig))
  return add_rating_data

def update_rating(existing_rating: UserBookRating, new_rating_value: int, db: Session):
  existing_rating.rating = new_rating_value
  try:
      db.commit()
      db.refresh(existing_rating)
  except IntegrityError as e:
      db.rollback()
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.orig))
  return existing_rating

def get_liked_book_ids_by_user_id(user_id: int, db: Session):
    liked_books = (
        db.query(UserBookRating)
        .with_entities(UserBookRating.book_id)
        .filter(UserBookRating.user_id == user_id)
        .filter(UserBookRating.rating > 3)
        .all()
    )

    return [book_id for (book_id,) in liked_books]

def get_book_title(book_title_filter: BookTitleFilter,  pagination: Pagination, db: Session):
  query = db.query(Book)
  
  if len(book_title_filter.title) != 0:
    print(f"book title filter: {book_title_filter.title}")
    query = query.filter(Book.title.ilike(f"%{book_title_filter.title}%"))
    
  books = (
    query
    .offset(pagination.skip)
    .limit(pagination.limit)
    .all()
  )
  
  total = query.count()
  
  return books, total