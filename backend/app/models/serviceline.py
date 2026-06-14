from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Line(Base):
    __tablename__ = 'lines'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    duration_minutes = Column(Integer, default=60)
    price = Column(Float, default=0.0)
    is_active = Column(Integer, default=1)

    work_schedules = relationship("WorkSchedule", back_populates="line", cascade="all, delete-orphan")
    reservations = relationship("Reservation", back_populates="line")

