from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import shutil
from datetime import datetime

from backend.database import get_db
from backend.schemas.worker import (
    WorkerProfileCreate,
    WorkerProfileUpdate,
    WorkerProfileResponse,
    WorkerSearchFilters
)
from backend.models.user import User
from backend.models.worker import WorkerProfile
from backend.core.security import get_current_active_user, require_role

router = APIRouter(prefix="/api/workers", tags=["Workers"])


@router.post("/profile", response_model=WorkerProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_worker_profile(
    profile_data: WorkerProfileCreate,
    current_user: User = Depends(require_role(["worker"])),
    db: Session = Depends(get_db)
):
    """Create worker profile (worker only)"""
    
    # Check if profile already exists
    existing_profile = db.query(WorkerProfile).filter(
        WorkerProfile.user_id == current_user.id
    ).first()
    
    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Worker profile already exists"
        )
    
    # Create profile
    new_profile = WorkerProfile(
        user_id=current_user.id,
        **profile_data.model_dump()
    )
    
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    
    # Add user details to response
    response = WorkerProfileResponse.model_validate(new_profile)
    response.full_name = current_user.full_name
    response.email = current_user.email
    response.phone = current_user.phone
    
    return response


@router.get("/profile/me", response_model=WorkerProfileResponse)
async def get_my_worker_profile(
    current_user: User = Depends(require_role(["worker"])),
    db: Session = Depends(get_db)
):
    """Get current worker's profile"""
    
    profile = db.query(WorkerProfile).filter(
        WorkerProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Worker profile not found"
        )
    
    # Add user details
    response = WorkerProfileResponse.model_validate(profile)
    response.full_name = current_user.full_name
    response.email = current_user.email
    response.phone = current_user.phone
    
    return response


@router.put("/profile", response_model=WorkerProfileResponse)
async def update_worker_profile(
    profile_data: WorkerProfileUpdate,
    current_user: User = Depends(require_role(["worker"])),
    db: Session = Depends(get_db)
):
    """Update worker profile"""
    
    profile = db.query(WorkerProfile).filter(
        WorkerProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Worker profile not found"
        )
    
    # Update fields
    update_data = profile_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)
    
    db.commit()
    db.refresh(profile)
    
    # Add user details
    response = WorkerProfileResponse.model_validate(profile)
    response.full_name = current_user.full_name
    response.email = current_user.email
    response.phone = current_user.phone
    
    return response


@router.get("/search", response_model=List[WorkerProfileResponse])
async def search_workers(
    skill: Optional[str] = None,
    location: Optional[str] = None,
    min_rating: Optional[float] = None,
    max_price: Optional[float] = None,
    availability: Optional[str] = None,
    is_available: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Search and filter workers"""
    
    query = db.query(WorkerProfile).join(User)
    
    # Apply filters
    if skill:
        query = query.filter(WorkerProfile.skills.contains(skill))
    
    if location:
        query = query.filter(WorkerProfile.location.contains(location))
    
    if min_rating is not None:
        query = query.filter(WorkerProfile.rating >= min_rating)
    
    if max_price is not None:
        query = query.filter(WorkerProfile.price_per_hour <= max_price)
    
    if availability:
        query = query.filter(WorkerProfile.availability == availability)
    
    if is_available is not None:
        query = query.filter(WorkerProfile.is_available == is_available)
    
    # Only show approved workers
    query = query.filter(User.is_approved == True, User.is_active == True)
    
    workers = query.all()
    
    # Add user details to each worker
    results = []
    for worker in workers:
        response = WorkerProfileResponse.model_validate(worker)
        response.full_name = worker.user.full_name
        response.email = worker.user.email
        response.phone = worker.user.phone
        results.append(response)
    
    return results


@router.get("/{worker_id}", response_model=WorkerProfileResponse)
async def get_worker_profile(worker_id: int, db: Session = Depends(get_db)):
    """Get specific worker profile by ID"""
    
    profile = db.query(WorkerProfile).filter(WorkerProfile.user_id == worker_id).first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Worker profile not found"
        )
    
    # Check if worker is approved
    if not profile.user.is_approved or not profile.user.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Worker not available"
        )
    
    # Add user details
    response = WorkerProfileResponse.model_validate(profile)
    response.full_name = profile.user.full_name
    response.email = profile.user.email
    response.phone = profile.user.phone
    
    return response


@router.post("/profile/upload-image")
async def upload_profile_image(
    file: UploadFile = File(...),
    current_user: User = Depends(require_role(["worker"])),
    db: Session = Depends(get_db)
):
    """Upload worker profile image"""
    
    profile = db.query(WorkerProfile).filter(
        WorkerProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Worker profile not found"
        )
    
    # Create uploads directory if it doesn't exist
    upload_dir = "uploads/profiles"
    os.makedirs(upload_dir, exist_ok=True)
    
    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1]
    filename = f"worker_{current_user.id}_{datetime.now().timestamp()}{file_extension}"
    file_path = os.path.join(upload_dir, filename)
    
    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Update profile
    profile.profile_image = file_path
    db.commit()
    
    return {"message": "Profile image uploaded successfully", "file_path": file_path}
