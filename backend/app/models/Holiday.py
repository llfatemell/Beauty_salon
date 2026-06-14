from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Holiday(Base):
    __tablename__ = 'holidays'

    id = Column(Integer, primary_key=True, autoincrement=True)
    holiday_date = Column(String, unique=True, nullable=False)   # DATE
    description = Column(Text)