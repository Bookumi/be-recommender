from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.book import BookFilter, BookResponse, SimiliarBookFilter, GetCFSVDRecommendation
from app.schemas.pagination import PaginatedResponse, Pagination
from app.schemas.response import BaseResponse
from app.crud import book as BookCRUD
import app.recommenders.faiss as FAISSRecommender
import app.recommenders.cf_svd as SVDRecommender

def get_all_books(
  book_filter: BookFilter,
  pagination: Pagination,
  db: Session
):
  books, total = BookCRUD.get_all_books(book_filter, pagination,  db)
  
  return books, total

def get_detail_book(id: int, db: Session):
  book = BookCRUD.get_detail_book(id, db)
  
  return book

def get_similiar_books(
  book_filter: SimiliarBookFilter,
  pagination: Pagination,
  db: Session
):
  similar_book_ids = []

  if book_filter.book_language_code == "ind":
    # Membuat vector untuk buku yang dicari
    book_idx = FAISSRecommender.book_id_to_idx_ind.get(book_filter.book_id)
    if book_idx is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book ID not found in FAISS index")

    book_vector = FAISSRecommender.faiss_index_ind.reconstruct(book_idx)

    # Mencari item dengan jarak vector terdekat
    distances, indices = FAISSRecommender.faiss_index_ind.search(book_vector.reshape(1, -1), book_filter.top_k + 1)
    indices = indices.flatten().tolist()

    # remove itself
    indices = [i for i in indices if i != book_idx]

    similar_book_ids = [FAISSRecommender.idx_to_book_id_ind[i] for i in indices]
  elif book_filter.book_language_code == "en":
    # Membuat vector untuk buku yang dicari
    book_idx = FAISSRecommender.book_id_to_idx_en.get(book_filter.book_id)
    if book_idx is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book ID not found in FAISS index")

    book_vector = FAISSRecommender.faiss_index_en.reconstruct(book_idx)

    # Mencari item dengan jarak vector terdekat
    distances, indices = FAISSRecommender.faiss_index_en.search(book_vector.reshape(1, -1), book_filter.top_k + 1)
    indices = indices.flatten().tolist()

    # remove itself
    indices = [i for i in indices if i != book_idx]

    similar_book_ids = [FAISSRecommender.idx_to_book_id_en[i] for i in indices]
  else:
     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"unrecognise book_language_code value: {book_filter.book_language_code}")
  
  
  books, total = BookCRUD.get_similiar_books(
    book_filter,
    pagination,
    similar_book_ids,
    db,
  )
  
  return books, total

def get_cf_svd_recommendation(
  get_recommendation_request: GetCFSVDRecommendation,
  pagination: Pagination,
  db: Session
):
  target_user: list[int]

  if SVDRecommender.svd_model is None or SVDRecommender.user_items is None:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="SVD model and user_items dict not load properly")
  
  # Case pertama, jika user_id ada di dalam user_items
  if get_recommendation_request["user_id"] in SVDRecommender.user_items:
    target_user = get_recommendation_request["user_id"]
  else:
    # Case kedua, jika tidak ada user_id di dalam user_items
    if not get_recommendation_request["liked_books"]:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="liked books is required for new users")
     
    user_with_same_liked = SVDRecommender.get_similiar_user(get_recommendation_request["liked_books"])

    if user_with_same_liked is None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user with similiar liked book not found")
     
    target_user = user_with_same_liked
     
  all_books = list({b for books in SVDRecommender.user_items.values() for b in books})
  read_books = set(SVDRecommender.user_items.get(target_user, []))
  unread_books = [b for b in all_books if b not in read_books]
   
  # Prediksi skor untuk buku yang belum dibaca
  predictions = [
    (book_id, SVDRecommender.svd_model.predict(target_user, book_id).est)
    for book_id in unread_books
  ]
  
	# Urutkan berdasarkan rating prediksi tertinggi
  top_recommendations = sorted(predictions, key=lambda x: x[1], reverse=True)[:pagination.limit]
  recommended_ids = [b for b, _ in top_recommendations]
  
  books, total = BookCRUD.get_similiar_books(None, pagination, recommended_ids, db)
  
  return books, total