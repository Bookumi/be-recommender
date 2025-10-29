from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.book import BookFilter, BookResponse, SimiliarBookFilter
from app.schemas.pagination import PaginatedResponse, Pagination
from app.schemas.response import BaseResponse
from app.crud import book as BookCRUD
import app.recommenders.faiss as recommender

router = APIRouter(prefix="/api/v1/books", tags=["Books"])

@router.get("", response_model=BaseResponse[PaginatedResponse[BookResponse]])
def get_all_books(
  book_filter: BookFilter = Depends(BookFilter.as_query),
  pagination: Pagination = Depends(),
  db: Session = Depends(get_db)
):
  books, total = BookCRUD.get_all_books(db, pagination, book_filter)
  return BaseResponse(
    message="success get all books",
    data=PaginatedResponse(
      total=total,
      page=pagination.page,
      limit=pagination.limit,
      items=books
    )
  )

@router.get("/similiar", response_model=BaseResponse[PaginatedResponse[BookResponse]])
def get_similiar_books(
  book_filter: SimiliarBookFilter = Depends(SimiliarBookFilter.as_query),
  pagination: Pagination = Depends(),
  db: Session = Depends(get_db)
):
  # Membuat vector untuk buku yang dicari
  print(type(list(recommender.book_id_to_idx.keys())[0]))
  book_idx = recommender.book_id_to_idx.get(book_filter.book_id)
  if book_idx is None:
      raise HTTPException(status_code=404, detail="Book ID not found in FAISS index")

  book_vector = recommender.faiss_index.reconstruct(book_idx)

  # Mencari item dengan jarak vector terdekat
  distances, indices = recommender.faiss_index.search(book_vector.reshape(1, -1), book_filter.top_k + 1)
  indices = indices.flatten().tolist()

  # remove itself
  indices = [i for i in indices if i != book_idx]

  similar_book_ids = [recommender.idx_to_book_id[i] for i in indices]

  # Gunakan book_id untuk query get book by ids
  books, total = BookCRUD.get_similiar_books(
    db,
    similar_book_ids,
    pagination,
    book_filter
  )

  return BaseResponse(
    message=f"success get similiar books of book_id ${book_filter.book_id}",
    data=PaginatedResponse(
      total=total,
      page=pagination.page,
      limit=pagination.limit,
      items=books
    )
  )

@router.get("/{id}", response_model=BaseResponse[BookResponse])
def get_detail_book(id: int, db: Session = Depends(get_db)):
  book = BookCRUD.get_detail_book(db, id)

  if not book:
    raise HTTPException(status_code=404, detail="book not found")

  return BaseResponse(
    message="success get detail book",
    data=book
  )
