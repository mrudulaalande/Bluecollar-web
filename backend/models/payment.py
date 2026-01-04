from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum as SQLEnum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database import Base
import enum


class PaymentStatus(str, enum.Enum):
    """Payment status enumeration"""
    PENDING = "Pending"
    SUCCESS = "Success"
    FAILED = "Failed"
    REFUNDED = "Refunded"


class PaymentMethod(str, enum.Enum):
    """Payment method enumeration"""
    RAZORPAY = "Razorpay"
    STRIPE = "Stripe"
    CASH = "Cash"


class Payment(Base):
    """Payment transaction model"""
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Relationships
    booking_id = Column(Integer, ForeignKey("bookings.id"), unique=True, nullable=False)
    client_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    worker_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Payment Details
    amount = Column(Float, nullable=False)
    payment_method = Column(SQLEnum(PaymentMethod), nullable=False)
    status = Column(SQLEnum(PaymentStatus), default=PaymentStatus.PENDING)
    
    # Gateway Details
    transaction_id = Column(String(255), unique=True, nullable=True)
    gateway_response = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    booking = relationship("Booking", backref="payment")
    client = relationship("User", foreign_keys=[client_id])
    worker = relationship("User", foreign_keys=[worker_id])
    
    def __repr__(self):
        return f"<Payment {self.id} booking={self.booking_id} amount={self.amount} status={self.status}>"
