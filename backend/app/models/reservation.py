from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Reservation(Base):
    __tablename__ = 'reservations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    reservation_code = Column(String, unique=True, nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.id', ondelete='CASCADE'), nullable=False)
    line_id = Column(Integer, ForeignKey('lines.id', ondelete='CASCADE'), nullable=False)
    reservation_date = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, default=60)
    total_price = Column(Float, nullable=False)
    status = Column(String, default='confirmed')  
    created_at = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime)                  

    __table_args__ = (
        CheckConstraint("status IN ('confirmed','cancelled','completed')", name='check_status'),
    )


    customer = relationship("Customer", back_populates="reservations")
    line = relationship("Line", back_populates="reservations")
