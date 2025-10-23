from sqlalchemy import Table, Column, Integer, ForeignKey
from app.database import Base

books_genres = Table(
  "books_genres",
  Base.metadata, 
  Column("book_id", Integer, ForeignKey("books.id", ondelete="CASCADE"), primary_key=True),
  Column("genre_id", Integer, ForeignKey("genres.id", ondelete="CASCADE"), primary_key=True),
)