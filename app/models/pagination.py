from pydantic import BaseModel, Field, computed_field

class Pagination(BaseModel):
  page: int = Field(1, ge=1, description="current page number")
  limit: int = Field(20, ge=1, le=100, description="maximum of item in each page")

  @computed_field
  @property
  def skip(self) -> int:
    # compute number of item to skip based on page and limit.
    return (self.page - 1) * self.limit