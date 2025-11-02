from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload
from app.models.user import User
from app.schemas.pagination import Pagination
from app.schemas.auth import LoginMethod
from typing import Union, Any


def get_user_detail(key: str, method: LoginMethod, db: Session):
  if method == LoginMethod.EMAIL:
    user = db.query(User).filter(User.email == key).first()
  elif method == LoginMethod.PHONE_NUMBER:
    user = db.query(User).filter(User.phone_number == key).first()
  else:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="not recognize login method please try again with email or phonenumber")
  
  return user