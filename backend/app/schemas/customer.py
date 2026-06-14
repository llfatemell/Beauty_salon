from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    email: Optional[EmailStr] = None
    birth_date: Optional[str] = None
    gender: Optional[str] = None
    address: Optional[str] = None
    notes: Optional[str] = None

class CustomerCreate(CustomerBase):
    password: str

class CustomerUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    birth_date: Optional[str] = None
    gender: Optional[str] = None
    address: Optional[str] = None
    notes: Optional[str] = None

class CustomerResponse(CustomerBase):
    id: int
    register_date: datetime
    total_visits: int
    phone_verified: int
    is_active: int
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True