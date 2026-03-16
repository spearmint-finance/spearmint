"""API routes for bank data aggregation (Plaid + Akoya)."""

import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..schemas.aggregator import (
    LinkTokenResponse,
    AkoyaAuthUrlResponse,
    PublicTokenExchange,
    AkoyaCallbackRequest,
    LinkedProviderResponse,
    SyncResultResponse,
)
from ...services.plaid_service import PlaidService
from ...services.akoya_service import AkoyaService
from ...services.aggregator_service import AggregatorService
from ...config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/link", tags=["link"])


# --- Plaid endpoints ---

@router.post("/plaid/token", response_model=LinkTokenResponse)
def create_plaid_link_token(db: Session = Depends(get_db)):
    """Create a Plaid Link token for the frontend."""
    if not settings.PLAID_CLIENT_ID:
        raise HTTPException(status_code=503, detail="Plaid is not configured")
    service = PlaidService(db)
    return service.create_link_token()


@router.post("/plaid/exchange", response_model=LinkedProviderResponse)
def exchange_plaid_token(
    request: PublicTokenExchange,
    db: Session = Depends(get_db),
):
    """Exchange a Plaid public token for an access token and create accounts."""
    if not settings.PLAID_CLIENT_ID:
        raise HTTPException(status_code=503, detail="Plaid is not configured")

    service = PlaidService(db)
    try:
        provider = service.exchange_public_token(
            public_token=request.public_token,
            institution_id=request.institution_id,
            institution_name=request.institution_name,
        )
        return _provider_to_response(provider)
    except Exception as e:
        logger.error(f"Plaid token exchange failed: {e}")
        raise HTTPException(status_code=400, detail=f"Failed to link account: {str(e)}")


# --- Akoya endpoints ---

@router.get("/akoya/authorize", response_model=AkoyaAuthUrlResponse)
def get_akoya_auth_url(
    provider_id: str = "fidelity",
    db: Session = Depends(get_db),
):
    """Get the Akoya OAuth authorization URL for user redirect."""
    if not settings.AKOYA_CLIENT_ID:
        raise HTTPException(status_code=503, detail="Akoya is not configured")
    service = AkoyaService(db)
    url = service.get_authorization_url(provider_id)
    return AkoyaAuthUrlResponse(authorization_url=url, provider_id=provider_id)


@router.post("/akoya/callback", response_model=LinkedProviderResponse)
def exchange_akoya_code(
    request: AkoyaCallbackRequest,
    db: Session = Depends(get_db),
):
    """Exchange an Akoya authorization code for tokens and create accounts."""
    if not settings.AKOYA_CLIENT_ID:
        raise HTTPException(status_code=503, detail="Akoya is not configured")

    service = AkoyaService(db)
    try:
        provider = service.exchange_auth_code(
            auth_code=request.auth_code,
            provider_id=request.provider_id,
        )
        return _provider_to_response(provider)
    except Exception as e:
        logger.error(f"Akoya auth code exchange failed: {e}")
        raise HTTPException(status_code=400, detail=f"Failed to link Fidelity account: {str(e)}")


# --- Provider management endpoints ---

@router.get("/providers", response_model=List[LinkedProviderResponse])
def list_providers(db: Session = Depends(get_db)):
    """List all linked data providers."""
    service = AggregatorService(db)
    providers = service.get_providers()
    return [_provider_to_response(p) for p in providers]


@router.get("/providers/{provider_id}", response_model=LinkedProviderResponse)
def get_provider(provider_id: int, db: Session = Depends(get_db)):
    """Get details for a specific linked provider."""
    service = AggregatorService(db)
    provider = service.get_provider(provider_id)
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    return _provider_to_response(provider)


@router.post("/providers/{provider_id}/sync", response_model=SyncResultResponse)
def sync_provider(provider_id: int, db: Session = Depends(get_db)):
    """Trigger a manual sync for a linked provider."""
    service = AggregatorService(db)
    try:
        result = service.sync(provider_id)
        return SyncResultResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Sync failed for provider {provider_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Sync failed: {str(e)}")


@router.delete("/providers/{provider_id}")
def unlink_provider(provider_id: int, db: Session = Depends(get_db)):
    """Unlink a provider. Keeps accounts and transactions but revokes access."""
    service = AggregatorService(db)
    try:
        service.unlink(provider_id)
        return {"message": "Provider unlinked successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# --- Plaid webhook ---

@router.post("/webhook/plaid")
def plaid_webhook(payload: dict, db: Session = Depends(get_db)):
    """Receive Plaid webhooks for automatic transaction sync."""
    webhook_type = payload.get('webhook_type', '')
    webhook_code = payload.get('webhook_code', '')
    item_id = payload.get('item_id', '')

    logger.info(f"Plaid webhook: type={webhook_type}, code={webhook_code}, item={item_id}")

    service = PlaidService(db)
    service.handle_webhook(webhook_type, webhook_code, item_id)
    return {"status": "ok"}


def _provider_to_response(provider) -> LinkedProviderResponse:
    """Convert a LinkedProvider model to response schema."""
    return LinkedProviderResponse(
        id=provider.id,
        provider_type=provider.provider_type,
        institution_id=provider.institution_id,
        institution_name=provider.institution_name,
        status=provider.status,
        error_code=provider.error_code,
        error_message=provider.error_message,
        last_synced_at=provider.last_synced_at,
        created_at=provider.created_at,
        account_count=len(provider.accounts) if provider.accounts else 0,
    )
