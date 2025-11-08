from fastapi import APIRouter, Depends
from app.schemas.response import BaseResponse
from app.schemas.user import UserPreferenceResponse, UserPreferenceRequest
from app.schemas.auth import JWTPayload
from app.middlewares.auth import verify_auth_token
import app.services.user as UserService 
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter(prefix="/api/v1/users", tags=["Users"])

@router.get("/preferences", response_model=BaseResponse[UserPreferenceResponse])
def get_user_preferences(
  current_user: JWTPayload = Depends(verify_auth_token),
  db: Session = Depends(get_db)
):
  user_prefferences = UserService.get_preferences_by_user_id(current_user.sub, db)
  
  return BaseResponse(
    message="success get user preferences",
    data=user_prefferences
  )
  
@router.post("/preferences", response_model=BaseResponse[UserPreferenceResponse])
def add_user_preferences(
  request_payload: UserPreferenceRequest,
  current_user: JWTPayload = Depends(verify_auth_token),
  db: Session = Depends(get_db)
):
  request_data = request_payload.model_copy(update={"user_id": current_user.sub})
  
  user_preference = UserService.add_user_preferences(current_user.sub, request_data, db)
  
  return BaseResponse(
    message="success add user preferences",
    data=user_preference
  )