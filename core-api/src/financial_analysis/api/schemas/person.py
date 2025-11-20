"""Pydantic schemas for Person endpoints."""

from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, Field


class PersonCreate(BaseModel):
    """Schema to create a person."""
    name: str = Field(..., max_length=100)
    is_active: bool = Field(default=True)


class PersonRead(BaseModel):
    """Schema returned for a person."""
    person_id: int
    name: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

