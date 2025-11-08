from pydantic import BaseModel

class UserPreferenceResponse(BaseModel):
  _user_id: int
  genres: list[str]
  languages: list[str]
  
class UserPreferenceRequest(BaseModel):
  genres: list[int]
  languages: list[str]
  
class UserGenrePreferenceRequest(BaseModel):
  user_id: str
  genres: list[int]

class UserLanguagePreferenceRequest(BaseModel):
  user_id: str
  languages: list[str]