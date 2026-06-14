from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AdminBase(BaseModel):
    username: str
    full_name: Optional[str] = None
    is_active: Optional[int] = 1

class AdminCreate(AdminBase):
    password: str

class AdminResponse(AdminBase):
    id: int
    created_at: datetime

    class Config:
       from_attributes = True