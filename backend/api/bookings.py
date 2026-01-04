from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from backend.database import get_db
from backend.schemas.booking import (
    BookingCreate,
    BookingUpdate,
    BookingResponse,
    BookingStatusUpdate
)
from backend.models.user import User
from backend.models.booking import Booking, BookingStatus
from backend.models.worker import WorkerProfile
from backend.core.security import get_current_active_user, require_role

router = APIRouter(prefix="/api/bookings", tags=["Bookings"])


@router.post("", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
async def create_booking(
    booking_data: BookingCreate,
    current_user: User = Depends(require_role(["client"])),
    db: Session = Depends(get_db)
):
    """Create a new booking (client only)"""
    
    # Get worker profile to calculate price
    worker_profile = db.query(WorkerProfile).filter(
        WorkerProfile.user_id == booking_data.worker_id
    ).first()
    
    if not worker_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Worker not found"
        )
    
    # Check if worker is available
    if worker_profile.is_available == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Worker is currently not available"
        )
    
    # Calculate total price
    total_price = booking_data.hours * worker_profile.price_per_hour
    
    # Check for booking conflicts (same worker, overlapping time)
    existing_booking = db.query(Booking).filter(
        Booking.worker_id == booking_data.worker_id,
        Booking.booking_date == booking_data.booking_date,
        Booking.status.in_([BookingStatus.PENDING, BookingStatus.ACCEPTED])
    ).first()
    
    if existing_booking:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Worker already has a booking at this time"
        )
    
    # Create booking
    new_booking = Booking(
        client_id=current_user.id,
        worker_id=booking_data.worker_id,
        booking_date=booking_data.booking_date,
        hours=booking_data.hours,
        total_price=total_price,
        description=booking_data.description,
        address=booking_data.address,
        status=BookingStatus.PENDING
    )
    
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    
    # Add additional info
    response = BookingResponse.model_validate(new_booking)
    response.client_name = current_user.full_name
    response.worker_name = worker_profile.user.full_name
    response.worker_skills = worker_profile.skills
    
    return response


@router.get("/my-bookings", response_model=List[BookingResponse])
async def get_my_bookings(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all bookings for current user (client or worker)"""
    
    if current_user.role == "client":
        bookings = db.query(Booking).filter(Booking.client_id == current_user.id).all()
    elif current_user.role == "worker":
        bookings = db.query(Booking).filter(Booking.worker_id == current_user.id).all()
    else:
        bookings = []
    
    # Add additional info
    results = []
    for booking in bookings:
        response = BookingResponse.model_validate(booking)
        response.client_name = booking.client.full_name
        response.worker_name = booking.worker.full_name
        
        worker_profile = db.query(WorkerProfile).filter(
            WorkerProfile.user_id == booking.worker_id
        ).first()
        if worker_profile:
            response.worker_skills = worker_profile.skills
        
        results.append(response)
    
    return results


@router.get("/{booking_id}", response_model=BookingResponse)
async def get_booking(
    booking_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get specific booking details"""
    
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    # Check authorization
    if current_user.role != "admin" and \
       booking.client_id != current_user.id and \
       booking.worker_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this booking"
        )
    
    # Add additional info
    response = BookingResponse.model_validate(booking)
    response.client_name = booking.client.full_name
    response.worker_name = booking.worker.full_name
    
    worker_profile = db.query(WorkerProfile).filter(
        WorkerProfile.user_id == booking.worker_id
    ).first()
    if worker_profile:
        response.worker_skills = worker_profile.skills
    
    return response


@router.put("/{booking_id}/status", response_model=BookingResponse)
async def update_booking_status(
    booking_id: int,
    status_update: BookingStatusUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update booking status"""
    
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    # Authorization checks
    if status_update.status == BookingStatus.ACCEPTED:
        # Only worker can accept
        if current_user.id != booking.worker_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only the assigned worker can accept this booking"
            )
    elif status_update.status == BookingStatus.CANCELLED:
        # Client or worker can cancel
        if current_user.id != booking.client_id and current_user.id != booking.worker_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to cancel this booking"
            )
    elif status_update.status == BookingStatus.COMPLETED:
        # Only worker can mark as completed
        if current_user.id != booking.worker_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only the assigned worker can complete this booking"
            )
    
    # Update status
    booking.status = status_update.status
    
    if status_update.status == BookingStatus.COMPLETED:
        booking.completed_at = datetime.utcnow()
    
    db.commit()
    db.refresh(booking)
    
    # Add additional info
    response = BookingResponse.model_validate(booking)
    response.client_name = booking.client.full_name
    response.worker_name = booking.worker.full_name
    
    worker_profile = db.query(WorkerProfile).filter(
        WorkerProfile.user_id == booking.worker_id
    ).first()
    if worker_profile:
        response.worker_skills = worker_profile.skills
    
    return response


@router.delete("/{booking_id}")
async def cancel_booking(
    booking_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Cancel a booking"""
    
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    # Only client can cancel their own bookings
    if current_user.id != booking.client_id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to cancel this booking"
        )
    
    # Can only cancel pending or accepted bookings
    if booking.status not in [BookingStatus.PENDING, BookingStatus.ACCEPTED]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot cancel booking with status: {booking.status}"
        )
    
    booking.status = BookingStatus.CANCELLED
    db.commit()
    
    return {"message": "Booking cancelled successfully"}
