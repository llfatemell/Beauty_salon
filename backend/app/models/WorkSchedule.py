from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()
class WorkSchedule(Base):
    __tablename__ = 'work_schedules'

    id = Column(Integer, primary_key=True, autoincrement=True)
    line_id = Column(Integer, ForeignKey('lines.id', ondelete='CASCADE'), nullable=False)
    weekday = Column(Integer, nullable=False)          # 0=دوشنبه ... 6=یکشنبه
    start_time = Column(String, nullable=False)        # "09:00"
    end_time = Column(String, nullable=False)          # "18:00"

    __table_args__ = (
        CheckConstraint('weekday BETWEEN 0 AND 6', name='check_weekday'),
    )

    line = relationship("Line", back_populates="work_schedules")
