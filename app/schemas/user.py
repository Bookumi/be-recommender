from pydantic import BaseModel

class UserPrefferenceResponse(BaseModel):
  genres: list[str]
  languages: list[str]