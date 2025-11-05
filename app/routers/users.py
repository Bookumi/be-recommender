from fastapi import APIRouter, Depends
from app.schemas.response import BaseResponse
from app.schemas.user import UserPrefferenceResponse
from app.schemas.auth import JWTPayload
from app.middlewares.auth import verify_auth_token
import app.services.user as UserService 
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter(prefix="/api/v1/users", tags=["Users"])

@router.get("/prefferences", response_model=BaseResponse[UserPrefferenceResponse])
def get_user_prefferences(
  current_user: JWTPayload = Depends(verify_auth_token),
  db: Session = Depends(get_db)
):
  user_prefferences = UserService.get_prefferences_by_user_id(current_user.sub, db)
  
  return BaseResponse(
    message="success get user prefference",
    data=user_prefferences
  )