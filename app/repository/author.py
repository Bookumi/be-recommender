from sqlalchemy.orm import Session
from app.schemas.author import AuthorFilter
from app.schemas.pagination import Pagination
from app.models.author import Author

def get_all_authors(author_filter: AuthorFilter, pagination: Pagination, db: Session):
  query = db.query(Author)
  
  
  if len(author_filter.author_name) != 0:
    print(f"author name filter: {author_filter.author_name}")
    query = query.filter(Author.name.ilike(f"%{author_filter.author_name}%"))
  
  authors = (
    query
    .offset(pagination.skip)
    .limit(pagination.limit)
    .all()
  )
  
  total = query.count()
  
  return authors, total