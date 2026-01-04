from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum as SQLEnum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database import Base
import enum


class BookingStatus(str, enum.Enum):
    """Booking status enumeration"""
    PENDING = "Pending"
    ACCEPTED = "Accepted"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


class Booking(Base):
    """Booking model for client-worker appointments"""
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Relationships
    client_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    worker_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Booking Details
    booking_date = Column(DateTime(timezone=True), nullable=False)
    hours = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(SQLEnum(BookingStatus), default=BookingStatus.PENDING)
    
    # Additional Info
    description = Column(Text, nullable=True)
    address = Column(Text, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    client = relationship("User", foreign_keys=[client_id], backref="client_bookings")
    worker = relationship("User", foreign_keys=[worker_id], backref="worker_bookings")
    
    def __repr__(self):
        return f"<Booking {self.id} client={self.client_id} worker={self.worker_id} status={self.status}>"
