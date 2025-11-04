from fastapi import HTTPException, status
from app.schemas.auth import Login, LoginMethod, Register
from sqlalchemy.orm import Session
from app.crud import user as UserCRUD
from app.schemas.auth import JWTPayload
from passlib.context import CryptContext
from app.models.user import User
from datetime import datetime, timedelta, timezone
import os
import jwt

from dotenv import load_dotenv

load_dotenv()

# User for login or authenticate_user.
def authenticate_user(login_request: Login, db: Session):
  # Get user data.
  if "@" in login_request.key:
    user = UserCRUD.get_user_detail(login_request.key, LoginMethod.EMAIL, db)
  else:
    user = UserCRUD.get_user_detail(login_request.key, LoginMethod.PHONE_NUMBER, db)
    
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
  
  # Verify password with hashed password
  pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

  is_verified = pwd_context.verify(login_request.password.encode('utf-8'), user.password)
  
  if not is_verified:
    if "@" in login_request.key:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="your email or password is wrong")
    else:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="your phonenumber or password is wrong")
  
  # Construct JWT token.
  generated_token = generate_jwt_token(user)
  
  return generated_token, user

def register_user(register_request: Register, db: Session):
  user = UserCRUD.create(register_request, db)
  generated_token = generate_jwt_token(user)
  
  
  return user, generated_token

def generate_jwt_token(user_data: User):
  access_token_expires = datetime.now(timezone.utc) + (timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRED_MINUTES"))))
  token_payload = {
    "sub": str(user_data.id),
    "email": user_data.email,
    "exp": access_token_expires
  }
  
  generated_token = jwt.encode(token_payload, os.getenv("SECRET_KEY"), os.getenv("ALGORITHM"))
  
  return generated_token
