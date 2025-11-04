from sqlalchemy import Column, UUID, Integer, String, Float, Text
from app.database import Base
class User(Base):
  __tablename__ = "users"
  id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  name = Column(String(50), unique=False, nullable=False)
  email = Column(String(50), unique=True, nullable=False)
  phone_number = Column(String(20), unique=True, nullable=True)
  password = Column(Text(), unique=True, nullable=False)