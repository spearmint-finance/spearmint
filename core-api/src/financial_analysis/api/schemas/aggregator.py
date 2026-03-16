"""Pydantic schemas for bank data aggregation (Plaid + Akoya)."""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class LinkTokenResponse(BaseModel):
    """Response from creating a Plaid Link token."""
    link_token: str
    expiration: str


class AkoyaAuthUrlResponse(BaseModel):
    """Response with Akoya OAuth authorization URL."""
    authorization_url: str
    provider_id: str


class PublicTokenExchange(BaseModel):
    """Request to exchange a Plaid public token."""
    public_token: str = Field(..., description="Plaid public token from Link")
    institution_id: Optional[str] = Field(None, description="Plaid institution ID")
    institution_name: Optional[str] = Field(None, description="Institution display name")


class AkoyaCallbackRequest(BaseModel):
    """Request to exchange an Akoya authorization code."""
    auth_code: str = Field(..., description="Authorization code from Akoya OAuth redirect")
    provider_id: str = Field(default="fidelity", description="Akoya provider ID")


class LinkedProviderResponse(BaseModel):
    """Response with linked provider details."""
    id: int
    provider_type: str
    institution_id: Optional[str]
    institution_name: Optional[str]
    status: str
    error_code: Optional[str]
    error_message: Optional[str]
    last_synced_at: Optional[datetime]
    created_at: datetime
    account_count: int = 0

    model_config = ConfigDict(from_attributes=True)


class SyncResultResponse(BaseModel):
    """Response from a sync operation."""
    transactions_added: int = 0
    transactions_modified: int = 0
    transactions_removed: int = 0
    balances_updated: int = 0
    holdings_updated: int = 0
