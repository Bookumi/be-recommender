from sqlalchemy import Table, Column, Integer, ForeignKey
from app.database import Base

authors_books = Table(
  "authors_books",
  Base.metadata, 
  Column("author_id", Integer, ForeignKey("authors.id", ondelete="CASCADE"), primary_key=True),
  Column("book_id", Integer, ForeignKey("books.id", ondelete="CASCADE"), primary_key=True),
)