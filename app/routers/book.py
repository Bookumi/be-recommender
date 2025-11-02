from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.book import BookFilter, BookResponse, SimiliarBookFilter, GetCFSVDRecommendation
from app.schemas.pagination import PaginatedResponse, Pagination
from app.schemas.response import BaseResponse
from app.crud import book as BookCRUD
import app.recommenders.faiss as FAISSRecommender
import app.recommenders.cf_svd as SVDRecommender

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
  similar_book_ids = []

  if book_filter.book_language_code == "ind":
    # Membuat vector untuk buku yang dicari
    book_idx = FAISSRecommender.book_id_to_idx_ind.get(book_filter.book_id)
    if book_idx is None:
        raise HTTPException(status_code=404, detail="Book ID not found in FAISS index")

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
        raise HTTPException(status_code=404, detail="Book ID not found in FAISS index")

    book_vector = FAISSRecommender.faiss_index_en.reconstruct(book_idx)

    # Mencari item dengan jarak vector terdekat
    distances, indices = FAISSRecommender.faiss_index_en.search(book_vector.reshape(1, -1), book_filter.top_k + 1)
    indices = indices.flatten().tolist()

    # remove itself
    indices = [i for i in indices if i != book_idx]

    similar_book_ids = [FAISSRecommender.idx_to_book_id_en[i] for i in indices]
  else:
     raise HTTPException(status_code=403, detail=f"unrecognise book_language_code value: {book_filter.book_language_code}")

  # Gunakan book_id untuk query get book by ids
  books, total = BookCRUD.get_similiar_books(
    db,
    similar_book_ids,
    pagination,
    book_filter
  )

  return BaseResponse(
    message=f"success get similiar books of book_id {book_filter.book_id}",
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

@router.get("/similiar/cf-svd", response_model=BaseResponse[PaginatedResponse[BookResponse]])
def get_cf_svd_recommendation(
  get_recommendation_request: GetCFSVDRecommendation = Depends(GetCFSVDRecommendation.as_query),
  pagination: Pagination = Depends(),
  db: Session = Depends(get_db)
):
  target_user: list[int]

  if SVDRecommender.svd_model is None or SVDRecommender.user_items is None:
    raise HTTPException(status_code=500, detail="SVD model and user_items dict not load properly")
  
  # Case pertama, jika user_id ada di dalam user_items
  if get_recommendation_request.user_id in SVDRecommender.user_items:
    target_user = get_recommendation_request.user_id
  else:
    # Case kedua, jika tidak ada user_id di dalam user_items
    if not get_recommendation_request.liked_books:
         raise HTTPException(status_code=400, detail="liked books is required for new users")
     
    user_with_same_liked = SVDRecommender.get_similiar_user(get_recommendation_request.liked_books)

    if user_with_same_liked is None:
       raise HTTPException(status_code=404, detail="user with similiar liked book not found")
     
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
  
  books, total = BookCRUD.get_similiar_books(db, recommended_ids, pagination, None)
  
  return BaseResponse(
  	message=f"success get recommended books for user with id {get_recommendation_request.user_id}",
  	data=PaginatedResponse(
  	  total=total,
  	  page=pagination.page,
  	  limit=pagination.limit,
  	  items=books
  	)
  )