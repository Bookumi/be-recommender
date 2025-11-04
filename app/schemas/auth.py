from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional
import re
from enum import Enum

class LoginMethod(Enum):
  EMAIL = "email"
  PHONE_NUMBER = "phone_number"
  
class JWTPayload(BaseModel):
  sub: int
  email: str
  exp: datetime

class LoginResponse(BaseModel):
  name: str
  email: str
  phonenumber: Optional[str]
  token: str
  
class Login(BaseModel):
  key: str = Field(..., min_length=1, description="mail or phone number") 
  password: str = Field(..., min_length=1, description="Password")
    
class Register(BaseModel):
    name: str = Field(..., description="Username")
    email: str = Field(..., description="Email")
    phone_number: Optional[str] = Field(..., description="Phone number")
    password: str = Field(..., description="Password with minimum 8 characters, one uppercase, one lowercase, one number, and one special character")
    
    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain at least one digit')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character')
        return v