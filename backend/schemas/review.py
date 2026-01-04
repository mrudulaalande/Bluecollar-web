from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ReviewBase(BaseModel):
    """Base review schema"""
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None


class ReviewCreate(ReviewBase):
    """Schema for creating review"""
    booking_id: int


class ReviewResponse(ReviewBase):
    """Schema for review response"""
    id: int
    booking_id: int
    client_id: int
    worker_id: int
    created_at: datetime
    
    # Additional info
    client_name: Optional[str] = None
    
    class Config:
        from_attributes = True
