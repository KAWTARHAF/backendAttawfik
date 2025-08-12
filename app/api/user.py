# app/api/user.py

from typing import List
from fastapi import APIRouter, HTTPException
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.controllers import user_controller

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("", response_model=UserResponse)
def create_user_route(user_data: UserCreate):
    """Create a new user."""
    try:
        return user_controller.create_user(user_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=List[UserResponse])
def get_users_route():
    """Get all users."""
    return user_controller.get_users()


@router.get("/{user_id}", response_model=UserResponse)
def get_user_route(user_id: str):
    """Get a single user by ID."""
    try:
        return user_controller.get_user_by_id(user_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{user_id}", response_model=UserResponse)
def update_user_route(user_id: str, update_data: UserUpdate):
    """Update a user's details."""
    try:
        return user_controller.update_user(user_id, update_data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{user_id}")
def delete_user_route(user_id: str):
    """Delete a user."""
    try:
        return user_controller.delete_user(user_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
