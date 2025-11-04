from passlib.context import CryptContext

def hash_password(plain_password: str):
  pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
  
  return pwd_context.hash(plain_password.encode('utf-8'))