from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from backend.models.booking import BookingStatus


class BookingBase(BaseModel):
    """Base booking schema"""
    worker_id: int
    booking_date: datetime
    hours: float = Field(..., gt=0)
    description: Optional[str] = None
    address: str


class BookingCreate(BookingBase):
    """Schema for creating booking"""
    pass


class BookingUpdate(BaseModel):
    """Schema for updating booking"""
    status: Optional[BookingStatus] = None
    booking_date: Optional[datetime] = None
    hours: Optional[float] = Field(None, gt=0)
    description: Optional[str] = None
    address: Optional[str] = None


class BookingResponse(BookingBase):
    """Schema for booking response"""
    id: int
    client_id: int
    total_price: float
    status: BookingStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    # Additional info
    client_name: Optional[str] = None
    worker_name: Optional[str] = None
    worker_skills: Optional[str] = None
    
    class Config:
        from_attributes = True


class BookingStatusUpdate(BaseModel):
    """Schema for updating booking status"""
    status: BookingStatus
