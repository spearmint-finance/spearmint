"""
Pydantic schemas for authentication-related API endpoints.

These schemas define the request/response models for API key management,
used by MCP server clients to authenticate with the Spearmint API.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class APIKeyCreate(BaseModel):
    """Schema for creating a new API key."""
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Descriptive name for the key (e.g., 'Claude Desktop')"
    )
    expires_at: Optional[datetime] = Field(
        None,
        description="Optional expiration date for the key"
    )


class APIKeyResponse(BaseModel):
    """Schema for API key responses (masked key)."""
    model_config = ConfigDict(from_attributes=True)

    key_id: int
    name: str
    key_prefix: str = Field(
        ...,
        description="Key prefix for identification (e.g., 'smint_live_xxxx')"
    )
    is_active: bool
    last_used_at: Optional[datetime]
    created_at: datetime
    expires_at: Optional[datetime]


class APIKeyCreatedResponse(BaseModel):
    """Schema for newly created API key (includes full key - shown only once)."""
    key_id: int
    name: str
    key: str = Field(
        ...,
        description="Full API key - shown only once at creation time"
    )
    key_prefix: str
    is_active: bool
    created_at: datetime
    expires_at: Optional[datetime]


class APIKeyValidateRequest(BaseModel):
    """Schema for validating an API key."""
    key: str = Field(
        ...,
        min_length=40,
        description="Full API key to validate"
    )


class APIKeyValidateResponse(BaseModel):
    """Schema for API key validation response."""
    valid: bool
    key_id: Optional[int] = None
    name: Optional[str] = None
    message: Optional[str] = None


class APIKeyListResponse(BaseModel):
    """Schema for list of API keys."""
    keys: List[APIKeyResponse]
    total: int
