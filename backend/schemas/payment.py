from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from backend.models.payment import PaymentStatus, PaymentMethod


class PaymentBase(BaseModel):
    """Base payment schema"""
    booking_id: int
    amount: float = Field(..., gt=0)
    payment_method: PaymentMethod


class PaymentCreate(PaymentBase):
    """Schema for creating payment"""
    pass


class PaymentUpdate(BaseModel):
    """Schema for updating payment"""
    status: Optional[PaymentStatus] = None
    transaction_id: Optional[str] = None
    gateway_response: Optional[str] = None


class PaymentResponse(PaymentBase):
    """Schema for payment response"""
    id: int
    client_id: int
    worker_id: int
    status: PaymentStatus
    transaction_id: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    # Additional info
    client_name: Optional[str] = None
    worker_name: Optional[str] = None
    
    class Config:
        from_attributes = True


class PaymentVerification(BaseModel):
    """Schema for payment verification"""
    payment_id: int
    transaction_id: str
    status: PaymentStatus
