from pydantic import BaseModel, Field
from typing import Optional
from backend.models.worker import AvailabilityType


class WorkerProfileBase(BaseModel):
    """Base worker profile schema"""
    skills: str = Field(..., description="Comma-separated skills")
    experience_years: int = Field(..., ge=0, le=50)
    location: str
    pincode: str = Field(..., min_length=5, max_length=10)
    availability: AvailabilityType
    price_per_hour: float = Field(..., gt=0)
    bio: Optional[str] = None


class WorkerProfileCreate(WorkerProfileBase):
    """Schema for creating worker profile"""
    pass


class WorkerProfileUpdate(BaseModel):
    """Schema for updating worker profile"""
    skills: Optional[str] = None
    experience_years: Optional[int] = Field(None, ge=0, le=50)
    location: Optional[str] = None
    pincode: Optional[str] = None
    availability: Optional[AvailabilityType] = None
    price_per_hour: Optional[float] = Field(None, gt=0)
    bio: Optional[str] = None
    is_available: Optional[int] = None


class WorkerProfileResponse(WorkerProfileBase):
    """Schema for worker profile response"""
    id: int
    user_id: int
    profile_image: Optional[str] = None
    rating: float
    total_reviews: int
    is_available: int
    
    # Include user details
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    
    class Config:
        from_attributes = True


class WorkerSearchFilters(BaseModel):
    """Schema for worker search filters"""
    skill: Optional[str] = None
    location: Optional[str] = None
    min_rating: Optional[float] = Field(None, ge=0, le=5)
    max_price: Optional[float] = Field(None, gt=0)
    availability: Optional[AvailabilityType] = None
    is_available: Optional[int] = None
