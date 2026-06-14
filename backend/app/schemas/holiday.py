from pydantic import BaseModel
from typing import Optional

class HolidayBase(BaseModel):
    holiday_date: str   # "YYYY-MM-DD"
    description: Optional[str] = None

class HolidayCreate(HolidayBase):
    pass

class HolidayResponse(HolidayBase):
    id: int

    class Config:
        from_attributes = True