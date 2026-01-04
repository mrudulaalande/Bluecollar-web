from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database import Base


class Review(Base):
    """Review and rating model"""
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Relationships
    booking_id = Column(Integer, ForeignKey("bookings.id"), unique=True, nullable=False)
    client_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    worker_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Review Details
    rating = Column(Integer, nullable=False)  # 1-5 stars
    comment = Column(Text, nullable=True)
    
    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    booking = relationship("Booking", backref="review")
    client = relationship("User", foreign_keys=[client_id])
    worker = relationship("User", foreign_keys=[worker_id], backref="reviews")
    
    def __repr__(self):
        return f"<Review booking={self.booking_id} rating={self.rating}>"
