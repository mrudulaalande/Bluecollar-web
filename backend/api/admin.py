from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict
from datetime import datetime, timedelta

from backend.database import get_db
from backend.schemas.user import UserResponse
from backend.models.user import User, UserRole
from backend.models.booking import Booking, BookingStatus
from backend.models.payment import Payment, PaymentStatus
from backend.models.worker import WorkerProfile
from backend.core.security import require_role

router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.get("/dashboard")
async def get_admin_dashboard(
    current_user: User = Depends(require_role(["admin"])),
    db: Session = Depends(get_db)
) -> Dict:
    """Get admin dashboard analytics"""
    
    # Total users by role
    total_clients = db.query(User).filter(User.role == UserRole.CLIENT).count()
    total_workers = db.query(User).filter(User.role == UserRole.WORKER).count()
    total_users = total_clients + total_workers
    
    # Total bookings by status
    total_bookings = db.query(Booking).count()
    pending_bookings = db.query(Booking).filter(Booking.status == BookingStatus.PENDING).count()
    completed_bookings = db.query(Booking).filter(Booking.status == BookingStatus.COMPLETED).count()
    
    # Revenue
    total_revenue = db.query(func.sum(Payment.amount)).filter(
        Payment.status == PaymentStatus.SUCCESS
    ).scalar() or 0
    
    # Pending worker approvals
    pending_workers = db.query(User).filter(
        User.role == UserRole.WORKER,
        User.is_approved == False
    ).count()
    
    # Recent bookings (last 7 days)
    week_ago = datetime.utcnow() - timedelta(days=7)
    recent_bookings = db.query(Booking).filter(
        Booking.created_at >= week_ago
    ).count()
    
    return {
        "total_users": total_users,
        "total_clients": total_clients,
        "total_workers": total_workers,
        "total_bookings": total_bookings,
        "pending_bookings": pending_bookings,
        "completed_bookings": completed_bookings,
        "total_revenue": round(total_revenue, 2),
        "pending_worker_approvals": pending_workers,
        "recent_bookings_7days": recent_bookings
    }


@router.get("/users", response_model=List[UserResponse])
async def get_all_users(
    role: str = None,
    current_user: User = Depends(require_role(["admin"])),
    db: Session = Depends(get_db)
):
    """Get all users with optional role filter"""
    
    query = db.query(User)
    
    if role:
        query = query.filter(User.role == role)
    
    users = query.all()
    return users


@router.put("/users/{user_id}/approve")
async def approve_user(
    user_id: int,
    current_user: User = Depends(require_role(["admin"])),
    db: Session = Depends(get_db)
):
    """Approve a worker account"""
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if user.role != UserRole.WORKER:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only worker accounts need approval"
        )
    
    user.is_approved = True
    db.commit()
    
    return {"message": f"Worker {user.full_name} approved successfully"}


@router.put("/users/{user_id}/suspend")
async def suspend_user(
    user_id: int,
    current_user: User = Depends(require_role(["admin"])),
    db: Session = Depends(get_db)
):
    """Suspend a user account"""
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if user.role == UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot suspend admin accounts"
        )
    
    user.is_active = False
    db.commit()
    
    return {"message": f"User {user.full_name} suspended successfully"}


@router.put("/users/{user_id}/activate")
async def activate_user(
    user_id: int,
    current_user: User = Depends(require_role(["admin"])),
    db: Session = Depends(get_db)
):
    """Activate a suspended user account"""
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.is_active = True
    db.commit()
    
    return {"message": f"User {user.full_name} activated successfully"}


@router.get("/bookings")
async def get_all_bookings(
    status: str = None,
    current_user: User = Depends(require_role(["admin"])),
    db: Session = Depends(get_db)
):
    """Get all bookings with optional status filter"""
    
    query = db.query(Booking)
    
    if status:
        query = query.filter(Booking.status == status)
    
    bookings = query.all()
    
    # Add additional info
    results = []
    for booking in bookings:
        worker_profile = db.query(WorkerProfile).filter(
            WorkerProfile.user_id == booking.worker_id
        ).first()
        
        results.append({
            "id": booking.id,
            "client_name": booking.client.full_name,
            "client_email": booking.client.email,
            "worker_name": booking.worker.full_name,
            "worker_email": booking.worker.email,
            "worker_skills": worker_profile.skills if worker_profile else None,
            "booking_date": booking.booking_date,
            "hours": booking.hours,
            "total_price": booking.total_price,
            "status": booking.status,
            "created_at": booking.created_at
        })
    
    return results


@router.get("/payments")
async def get_all_payments(
    current_user: User = Depends(require_role(["admin"])),
    db: Session = Depends(get_db)
):
    """Get all payment transactions"""
    
    payments = db.query(Payment).all()
    
    # Add additional info
    results = []
    for payment in payments:
        results.append({
            "id": payment.id,
            "booking_id": payment.booking_id,
            "client_name": payment.client.full_name,
            "worker_name": payment.worker.full_name,
            "amount": payment.amount,
            "payment_method": payment.payment_method,
            "status": payment.status,
            "transaction_id": payment.transaction_id,
            "created_at": payment.created_at
        })
    
    return results


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(require_role(["admin"])),
    db: Session = Depends(get_db)
):
    """Delete a user account (use with caution)"""
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if user.role == UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete admin accounts"
        )
    
    db.delete(user)
    db.commit()
    
    return {"message": f"User {user.full_name} deleted successfully"}
