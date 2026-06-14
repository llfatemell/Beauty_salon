from pydantic import BaseModel
from typing import Optional

class LineBase(BaseModel):
    name: str
    duration_minutes: int = 60
    price: float = 0.0
    is_active: int = 1

class LineCreate(LineBase):
    pass

class LineUpdate(BaseModel):
    name: Optional[str] = None
    duration_minutes: Optional[int] = None
    price: Optional[float] = None
    is_active: Optional[int] = None

class LineResponse(LineBase):
    id: int

    class Config:
        from_attributes = True