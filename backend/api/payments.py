from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import json

from backend.database import get_db
from backend.schemas.payment import PaymentCreate, PaymentResponse, PaymentVerification
from backend.models.user import User
from backend.models.payment import Payment, PaymentStatus, PaymentMethod
from backend.models.booking import Booking
from backend.core.security import get_current_active_user, require_role
from backend.core.config import settings

router = APIRouter(prefix="/api/payments", tags=["Payments"])


@router.post("", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
async def create_payment(
    payment_data: PaymentCreate,
    current_user: User = Depends(require_role(["client"])),
    db: Session = Depends(get_db)
):
    """Create a payment for a booking (client only)"""
    
    # Get booking
    booking = db.query(Booking).filter(Booking.id == payment_data.booking_id).first()
    
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    # Verify booking belongs to current user
    if booking.client_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to pay for this booking"
        )
    
    # Check if payment already exists
    existing_payment = db.query(Payment).filter(
        Payment.booking_id == payment_data.booking_id
    ).first()
    
    if existing_payment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment already exists for this booking"
        )
    
    # Verify amount matches booking total
    if payment_data.amount != booking.total_price:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment amount does not match booking total"
        )
    
    # Create payment
    new_payment = Payment(
        booking_id=payment_data.booking_id,
        client_id=current_user.id,
        worker_id=booking.worker_id,
        amount=payment_data.amount,
        payment_method=payment_data.payment_method,
        status=PaymentStatus.PENDING
    )
    
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    
    # Add additional info
    response = PaymentResponse.model_validate(new_payment)
    response.client_name = current_user.full_name
    response.worker_name = booking.worker.full_name
    
    return response


@router.post("/{payment_id}/verify", response_model=PaymentResponse)
async def verify_payment(
    payment_id: int,
    verification: PaymentVerification,
    current_user: User = Depends(require_role(["client"])),
    db: Session = Depends(get_db)
):
    """Verify payment after gateway processing"""
    
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    
    # Verify payment belongs to current user
    if payment.client_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to verify this payment"
        )
    
    # Update payment status
    payment.status = verification.status
    payment.transaction_id = verification.transaction_id
    payment.gateway_response = json.dumps({"verified_at": str(verification)})
    
    db.commit()
    db.refresh(payment)
    
    # Add additional info
    booking = db.query(Booking).filter(Booking.id == payment.booking_id).first()
    response = PaymentResponse.model_validate(payment)
    response.client_name = current_user.full_name
    response.worker_name = booking.worker.full_name
    
    return response


@router.get("/my-payments", response_model=List[PaymentResponse])
async def get_my_payments(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all payments for current user"""
    
    if current_user.role == "client":
        payments = db.query(Payment).filter(Payment.client_id == current_user.id).all()
    elif current_user.role == "worker":
        payments = db.query(Payment).filter(Payment.worker_id == current_user.id).all()
    else:
        payments = []
    
    # Add additional info
    results = []
    for payment in payments:
        response = PaymentResponse.model_validate(payment)
        response.client_name = payment.client.full_name
        response.worker_name = payment.worker.full_name
        results.append(response)
    
    return results


@router.get("/{payment_id}", response_model=PaymentResponse)
async def get_payment(
    payment_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get specific payment details"""
    
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    
    # Check authorization
    if current_user.role != "admin" and \
       payment.client_id != current_user.id and \
       payment.worker_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this payment"
        )
    
    # Add additional info
    response = PaymentResponse.model_validate(payment)
    response.client_name = payment.client.full_name
    response.worker_name = payment.worker.full_name
    
    return response


@router.get("/booking/{booking_id}", response_model=PaymentResponse)
async def get_payment_by_booking(
    booking_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get payment for a specific booking"""
    
    payment = db.query(Payment).filter(Payment.booking_id == booking_id).first()
    
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found for this booking"
        )
    
    # Check authorization
    if current_user.role != "admin" and \
       payment.client_id != current_user.id and \
       payment.worker_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this payment"
        )
    
    # Add additional info
    response = PaymentResponse.model_validate(payment)
    response.client_name = payment.client.full_name
    response.worker_name = payment.worker.full_name
    
    return response
