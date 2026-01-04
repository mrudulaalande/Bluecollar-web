from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db
from backend.schemas.review import ReviewCreate, ReviewResponse
from backend.models.user import User
from backend.models.review import Review
from backend.models.booking import Booking, BookingStatus
from backend.models.worker import WorkerProfile
from backend.core.security import get_current_active_user, require_role

router = APIRouter(prefix="/api/reviews", tags=["Reviews"])


@router.post("", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_review(
    review_data: ReviewCreate,
    current_user: User = Depends(require_role(["client"])),
    db: Session = Depends(get_db)
):
    """Create a review for a completed booking (client only)"""
    
    # Get booking
    booking = db.query(Booking).filter(Booking.id == review_data.booking_id).first()
    
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    # Verify booking belongs to current user
    if booking.client_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to review this booking"
        )
    
    # Check if booking is completed
    if booking.status != BookingStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only review completed bookings"
        )
    
    # Check if review already exists
    existing_review = db.query(Review).filter(
        Review.booking_id == review_data.booking_id
    ).first()
    
    if existing_review:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Review already exists for this booking"
        )
    
    # Create review
    new_review = Review(
        booking_id=review_data.booking_id,
        client_id=current_user.id,
        worker_id=booking.worker_id,
        rating=review_data.rating,
        comment=review_data.comment
    )
    
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    
    # Update worker's rating
    update_worker_rating(booking.worker_id, db)
    
    # Add additional info
    response = ReviewResponse.model_validate(new_review)
    response.client_name = current_user.full_name
    
    return response


@router.get("/worker/{worker_id}", response_model=List[ReviewResponse])
async def get_worker_reviews(worker_id: int, db: Session = Depends(get_db)):
    """Get all reviews for a specific worker"""
    
    reviews = db.query(Review).filter(Review.worker_id == worker_id).all()
    
    # Add additional info
    results = []
    for review in reviews:
        response = ReviewResponse.model_validate(review)
        response.client_name = review.client.full_name
        results.append(response)
    
    return results


@router.get("/my-reviews", response_model=List[ReviewResponse])
async def get_my_reviews(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get reviews given by current user (if client) or received (if worker)"""
    
    if current_user.role == "client":
        reviews = db.query(Review).filter(Review.client_id == current_user.id).all()
    elif current_user.role == "worker":
        reviews = db.query(Review).filter(Review.worker_id == current_user.id).all()
    else:
        reviews = []
    
    # Add additional info
    results = []
    for review in reviews:
        response = ReviewResponse.model_validate(review)
        response.client_name = review.client.full_name
        results.append(response)
    
    return results


def update_worker_rating(worker_id: int, db: Session):
    """Update worker's average rating and total reviews"""
    
    # Get all reviews for worker
    reviews = db.query(Review).filter(Review.worker_id == worker_id).all()
    
    if not reviews:
        return
    
    # Calculate average rating
    total_rating = sum(review.rating for review in reviews)
    average_rating = total_rating / len(reviews)
    
    # Update worker profile
    worker_profile = db.query(WorkerProfile).filter(
        WorkerProfile.user_id == worker_id
    ).first()
    
    if worker_profile:
        worker_profile.rating = round(average_rating, 2)
        worker_profile.total_reviews = len(reviews)
        db.commit()
