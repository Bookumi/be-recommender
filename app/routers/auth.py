from fastapi import APIRouter, Depends, HTTPException, status, Response
from app.schemas.response import BaseResponse
from app.schemas.auth import LoginResponse, Login, Register
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

@router.post("/register", response_model=BaseResponse[LoginResponse])
def register(
  register_request: Register,
  db: Session = Depends(get_db)
):
  user, generated_token = AuthService.register_user(register_request, db)
  
  return BaseResponse(
    message="success register a new user",
    data=LoginResponse(
      name=user.name,
      email=user.email,
      phonenumber=user.phone_number,
      token=generated_token
    )
  )
  
@router.post("/logout")
def logout(response: Response):
  response.delete_cookie(key="access_token")  # name of your cookie
  return BaseResponse(
    message="success logout",
    data=None
  )