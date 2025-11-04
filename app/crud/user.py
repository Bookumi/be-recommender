from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload
from app.models.user import User
from app.schemas.pagination import Pagination
from app.schemas.auth import LoginMethod, Register
from typing import Union, Any
from sqlalchemy.exc import IntegrityError


def get_user_detail(key: str, method: LoginMethod, db: Session):
  if method == LoginMethod.EMAIL:
    user = db.query(User).filter(User.email == key).first()
  elif method == LoginMethod.PHONE_NUMBER:
    user = db.query(User).filter(User.phone_number == key).first()
  else:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="not recognize login method please try again with email or phonenumber")
  
  return user

def create(new_user_data: Register, db: Session):
  try:
    db.add(new_user_data)
    db.commit()
    db.refresh(new_user_data)
  except IntegrityError as e:
    db.rollback()
    if "email" in str(e.orig) and "exists" in str(e.orig):
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email already exists")
    elif "phone" in str(e.orig) and "exists" in str(e.orig):
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="phone number already exists")
    else:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.orig))

    
  return new_user_data