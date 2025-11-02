from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.response import BaseResponse
from app.schemas.auth import LoginResponse, Login
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import auth as AuthService

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])

@router.get("/login", response_model=BaseResponse[LoginResponse])
def login(
  login_request: Login = Depends(),
  db: Session = Depends(get_db)
):
  token, user = AuthService.authenticate_user(login_request, db)
  
  if not token:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="token not generated properly")
  
  return BaseResponse(
    message="success login and get auth token",
    data=LoginResponse(
      name=user.name,
      email=user.email,
      phonenumber=user.phone_number,
      token=token,
    )
  )