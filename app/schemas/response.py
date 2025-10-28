from typing import Generic, TypeVar
from pydantic.generics import GenericModel

T = TypeVar("T")

class BaseResponse(GenericModel, Generic[T]):
  message: str
  data: T