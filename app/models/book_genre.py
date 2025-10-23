from sqlalchemy import Table, Column, Integer, ForeignKey

books_genres = Table(
  "books_genres",
  Column("book_id", Integer, ForeignKey("book.id", ondelete="CASCADE"), primary_key=True),
  Column("genre_id", Integer, ForeignKey("genre.id", ondelete="CASCADE"), primary_key=True),
)