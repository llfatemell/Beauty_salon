from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ReservationBase(BaseModel):
    line_id: int
    reservation_date: datetime
    duration_minutes: Optional[int] = None
    total_price: Optional[float] = None

class ReservationCreate(ReservationBase):
    customer_id: int   

class ReservationUpdate(BaseModel):
    reservation_date: Optional[datetime] = None
    status: Optional[str] = None   # 'confirmed', 'cancelled', 'completed'

class ReservationResponse(ReservationBase):
    id: int
    reservation_code: str
    customer_id: int
    status: str
    created_at: datetime
    end_time: Optional[datetime] = None

    class Config:
        from_attributes = True