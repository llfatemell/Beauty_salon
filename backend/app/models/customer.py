from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    register_date = Column(DateTime, default=datetime.utcnow)
    total_visits = Column(Integer, default=0)
    notes = Column(Text)
    password_hash = Column(String, nullable=False, default='')
    email = Column(String, unique=True)
    phone_verified = Column(Integer, default=0)
    reset_token = Column(String)
    reset_token_expiry = Column(DateTime)
    last_login = Column(DateTime)
    birth_date = Column(String)       
    gender = Column(String)
    address = Column(Text)
    is_active = Column(Integer, default=1)

    reservations = relationship("Reservation", back_populates="customer", cascade="all, delete-orphan")
