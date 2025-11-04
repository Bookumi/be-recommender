from fastapi import status, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.schemas.auth import JWTPayload
from dotenv import load_dotenv
import os
import jwt

load_dotenv()
security = HTTPBearer()

def verify_auth_token(credentials: HTTPAuthorizationCredentials = Security(security)):
  if not credentials:
      raise HTTPException(
          status_code=status.HTTP_403_FORBIDDEN,
          detail="Authorization credentials missing"
      )
  
  token = credentials.credentials

  try:
    decoded_token = jwt.decode(
        token,
        key=os.getenv("SECRET_KEY"),
        algorithms=[os.getenv("ALGORITHM") or "HS256"]
    )

    return JWTPayload(**decoded_token)    
  except jwt.ExpiredSignatureError:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
  except jwt.InvalidTokenError as e:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid or malformed token: {str(e)}")
