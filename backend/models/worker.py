from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from backend.database import Base
import enum


class AvailabilityType(str, enum.Enum):
    """Worker availability types"""
    FULL_TIME = "Full-time"
    PART_TIME = "Part-time"
    WEEKENDS = "Weekends"


class WorkerProfile(Base):
    """Worker profile with professional details"""
    __tablename__ = "worker_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    # Professional Details
    skills = Column(Text, nullable=False)  # Comma-separated skills
    experience_years = Column(Integer, nullable=False)
    location = Column(String(255), nullable=False)
    pincode = Column(String(10), nullable=False)
    availability = Column(SQLEnum(AvailabilityType), nullable=False)
    price_per_hour = Column(Float, nullable=False)
    
    # Profile
    bio = Column(Text, nullable=True)
    profile_image = Column(String(500), nullable=True)
    
    # Ratings (auto-calculated)
    rating = Column(Float, default=0.0)
    total_reviews = Column(Integer, default=0)
    
    # Status
    is_available = Column(Integer, default=1)  # 1=available, 0=busy
    
    # Relationship
    user = relationship("User", backref="worker_profile")
    
    def __repr__(self):
        return f"<WorkerProfile user_id={self.user_id} skills={self.skills}>"
