from pydantic import BaseModel

class WorkScheduleBase(BaseModel):
    line_id: int
    weekday: int   # 0-6
    start_time: str
    end_time: str

class WorkScheduleCreate(WorkScheduleBase):
    pass

class WorkScheduleResponse(WorkScheduleBase):
    id: int

    class Config:
        from_attributes = True