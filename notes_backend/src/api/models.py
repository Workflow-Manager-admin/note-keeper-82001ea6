from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# PUBLIC_INTERFACE
class UserCreate(BaseModel):
    """Schema for creating a new user (registration)."""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=6, description="User password")


# PUBLIC_INTERFACE
class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=6, description="User password")


# PUBLIC_INTERFACE
class UserOut(BaseModel):
    """Schema for user data returned to frontend (except password)"""
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


# PUBLIC_INTERFACE
class NoteBase(BaseModel):
    """Base schema for note fields."""
    title: str = Field(..., description="Note title")
    content: str = Field(..., description="Note content")


# PUBLIC_INTERFACE
class NoteCreate(NoteBase):
    """Schema for creating a new note."""
    pass


# PUBLIC_INTERFACE
class NoteUpdate(BaseModel):
    """Schema for updating a note."""
    title: Optional[str] = Field(None, description="Note title")
    content: Optional[str] = Field(None, description="Note content")


# PUBLIC_INTERFACE
class NoteOut(NoteBase):
    """Schema for note output."""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
