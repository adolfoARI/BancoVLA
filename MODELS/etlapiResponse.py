from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    codigo:int =0
    mensaje:str ="Transaccion exitosa"
    data: Optional[T] = None # el objeto o lista que yo devuelvo