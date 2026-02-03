"""
API routes for authentication and API key management.

Provides endpoints for:
- Creating API keys for MCP server clients
- Listing and viewing API keys
- Validating API keys
- Revoking API keys
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ...services.auth_service import AuthService
from ..schemas.auth import (
    APIKeyCreate,
    APIKeyResponse,
    APIKeyCreatedResponse,
    APIKeyValidateRequest,
    APIKeyValidateResponse,
    APIKeyListResponse,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/api-keys", response_model=APIKeyCreatedResponse)
def create_api_key(
    key_data: APIKeyCreate,
    db: Session = Depends(get_db)
):
    """
    Generate a new API key.

    **Important:** The full API key is only returned once at creation time.
    Store it securely as it cannot be retrieved again.

    The key can be used to authenticate MCP server clients (Claude Desktop,
    Gemini CLI, ChatGPT) against the Spearmint API.
    """
    service = AuthService(db)

    try:
        api_key, full_key = service.create_key(
            name=key_data.name,
            expires_at=key_data.expires_at
        )

        return APIKeyCreatedResponse(
            key_id=api_key.key_id,
            name=api_key.name,
            key=full_key,
            key_prefix=api_key.key_prefix,
            is_active=api_key.is_active,
            created_at=api_key.created_at,
            expires_at=api_key.expires_at
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/api-keys", response_model=APIKeyListResponse)
def list_api_keys(
    include_inactive: bool = Query(
        False,
        description="Include revoked/inactive keys"
    ),
    db: Session = Depends(get_db)
):
    """
    List all API keys.

    Returns API keys with masked key values (only prefix is shown).
    """
    service = AuthService(db)
    keys = service.get_keys(include_inactive=include_inactive)

    return APIKeyListResponse(
        keys=[APIKeyResponse.model_validate(k) for k in keys],
        total=len(keys)
    )


@router.get("/api-keys/{key_id}", response_model=APIKeyResponse)
def get_api_key(
    key_id: int = Path(..., description="API key ID"),
    db: Session = Depends(get_db)
):
    """
    Get a specific API key by ID.

    Returns the API key metadata with masked key value.
    """
    service = AuthService(db)
    api_key = service.get_key(key_id)

    if not api_key:
        raise HTTPException(status_code=404, detail="API key not found")

    return APIKeyResponse.model_validate(api_key)


@router.delete("/api-keys/{key_id}")
def revoke_api_key(
    key_id: int = Path(..., description="API key ID"),
    permanent: bool = Query(
        False,
        description="Permanently delete instead of just revoking"
    ),
    db: Session = Depends(get_db)
):
    """
    Revoke or delete an API key.

    By default, keys are soft-deleted (revoked but kept in the database).
    Use `permanent=true` to permanently delete the key.
    """
    service = AuthService(db)

    if permanent:
        success = service.delete_key(key_id)
        if not success:
            raise HTTPException(status_code=404, detail="API key not found")
        return {"message": "API key permanently deleted", "key_id": key_id}
    else:
        success = service.revoke_key(key_id)
        if not success:
            raise HTTPException(status_code=404, detail="API key not found")
        return {"message": "API key revoked", "key_id": key_id}


@router.post("/api-keys/validate", response_model=APIKeyValidateResponse)
def validate_api_key(
    request: APIKeyValidateRequest,
    db: Session = Depends(get_db)
):
    """
    Validate an API key.

    This endpoint is used by the MCP server to validate incoming requests.
    It also updates the last_used_at timestamp for the key.
    """
    service = AuthService(db)
    is_valid, api_key, error_message = service.validate_key(request.key)

    if is_valid and api_key:
        return APIKeyValidateResponse(
            valid=True,
            key_id=api_key.key_id,
            name=api_key.name
        )
    else:
        return APIKeyValidateResponse(
            valid=False,
            message=error_message
        )
