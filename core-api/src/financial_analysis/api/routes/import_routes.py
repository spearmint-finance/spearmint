"""Import API endpoints."""

from pathlib import Path
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query, Path as PathParam
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..schemas.import_schema import (
    ImportRequest,
    ImportResponse,
    ImportHistoryResponse,
    ImportHistoryItem,
    ImportHistoryDetailResponse,
    ImportStatusResponse,
    ImportProfileCreate,
    ImportProfileUpdate,
    ImportProfileResponse,
    ImportProfileListResponse,
    ImportProfileSuggestion
)
from ...services.import_service import ImportService
from ...config import settings
from ...database.models import ImportHistory

router = APIRouter()


@router.post("/import", response_model=ImportResponse)
async def import_transactions(
    file: UploadFile = File(..., description="Excel file to import"),
    mode: str = Form("incremental", pattern="^(full|incremental|update)$", description="Import mode"),
    skip_duplicates: bool = Form(True, description="Skip duplicate transactions"),
    profile_id: Optional[int] = Form(None, description="Import profile ID to apply saved column mappings"),
    db: Session = Depends(get_db)
):
    """
    Import transactions from Excel file.

    Args:
        file: Uploaded Excel file
        mode: Import mode (full, incremental, update)
        skip_duplicates: Whether to skip duplicates
        profile_id: Optional import profile ID for column mappings
        db: Database session

    Returns:
        ImportResponse: Import result
    """
    # Validate file type
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only .xlsx and .xls files are supported."
        )

    # Check file size
    contents = await file.read()
    if len(contents) > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size is {settings.MAX_UPLOAD_SIZE} bytes."
        )

    # Save uploaded file temporarily
    temp_dir = settings.BASE_DIR / "data" / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    temp_file_path = temp_dir / file.filename

    try:
        # Write file
        with open(temp_file_path, 'wb') as f:
            f.write(contents)

        # Import transactions
        service = ImportService(db)
        result = service.import_from_excel(
            file_path=str(temp_file_path),
            mode=mode,
            skip_duplicates=skip_duplicates,
            profile_id=profile_id
        )

        # Convert result to response
        return ImportResponse(**result.to_dict())

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to import file: {str(e)}"
        )
    finally:
        # Clean up temporary file
        # Add retry logic for Windows file locking issues
        if temp_file_path.exists():
            import time
            for attempt in range(3):
                try:
                    temp_file_path.unlink()
                    break
                except PermissionError:
                    if attempt < 2:
                        time.sleep(0.1)  # Wait 100ms before retry
                    else:
                        # Log warning but don't fail the request
                        import logging
                        logging.getLogger(__name__).warning("Could not delete temp file %s", temp_file_path)


@router.post("/import/file-path", response_model=ImportResponse)
def import_from_file_path(
    file_path: str,
    request: ImportRequest,
    db: Session = Depends(get_db)
):
    """
    Import transactions from file path (for local development).
    
    Args:
        file_path: Path to Excel file
        request: Import request parameters
        db: Database session
        
    Returns:
        ImportResponse: Import result
    """
    # Verify file exists
    path = Path(file_path)
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"File not found: {file_path}")
    
    if not path.suffix.lower() in ['.xlsx', '.xls']:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only .xlsx and .xls files are supported."
        )
    
    try:
        service = ImportService(db)
        result = service.import_from_excel(
            file_path=file_path,
            mode=request.mode,
            skip_duplicates=request.skip_duplicates
        )
        
        return ImportResponse(**result.to_dict())
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to import file: {str(e)}"
        )

@router.get("/import/history", response_model=ImportHistoryResponse)
def get_import_history(
    limit: int = Query(50, ge=1, le=200, description="Maximum number of imports to return"),
    offset: int = Query(0, ge=0, description="Number of imports to skip"),
    db: Session = Depends(get_db)
):
    """
    Get import history.

    Returns a list of past imports with statistics including:
    - Import date and file name
    - Total rows, successful rows, failed rows
    - Classification statistics
    - Success rate

    Args:
        limit: Maximum number of imports to return
        offset: Number of imports to skip (for pagination)
        db: Database session

    Returns:
        ImportHistoryResponse: List of import history items
    """
    # Query import history
    query = db.query(ImportHistory).order_by(ImportHistory.import_date.desc())

    # Get total count
    total = query.count()

    # Apply pagination
    imports = query.offset(offset).limit(limit).all()

    # Convert to response items
    import_items = []
    for imp in imports:
        success_rate = (imp.successful_rows / imp.total_rows * 100) if imp.total_rows > 0 else 0.0
        import_items.append(ImportHistoryItem(
            import_id=imp.import_id,
            import_date=imp.import_date,
            file_name=imp.file_name,
            total_rows=imp.total_rows,
            successful_rows=imp.successful_rows,
            failed_rows=imp.failed_rows,
            classified_rows=imp.classified_rows,
            import_mode=imp.import_mode,
            success_rate=success_rate
        ))

    return ImportHistoryResponse(
        imports=import_items,
        total=total
    )


@router.get("/import/history/{import_id}", response_model=ImportHistoryDetailResponse)
def get_import_detail(
    import_id: int,
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific import.

    Returns detailed information including error logs and full statistics.

    Args:
        import_id: Import ID
        db: Database session

    Returns:
        ImportHistoryDetailResponse: Detailed import information
    """
    imp = db.query(ImportHistory).filter(ImportHistory.import_id == import_id).first()

    if not imp:
        raise HTTPException(status_code=404, detail=f"Import {import_id} not found")

    success_rate = (imp.successful_rows / imp.total_rows * 100) if imp.total_rows > 0 else 0.0

    return ImportHistoryDetailResponse(
        import_id=imp.import_id,
        import_date=imp.import_date,
        file_name=imp.file_name,
        file_path=imp.file_path,
        total_rows=imp.total_rows,
        successful_rows=imp.successful_rows,
        failed_rows=imp.failed_rows,
        classified_rows=imp.classified_rows,
        import_mode=imp.import_mode,
        error_log=imp.error_log,
        success_rate=success_rate
    )


@router.get("/import/status/{import_id}", response_model=ImportStatusResponse)
def get_import_status(
    import_id: int,
    db: Session = Depends(get_db)
):
    """
    Get real-time import status.

    This endpoint provides progress tracking for ongoing imports.
    For completed imports, it returns the final status.

    Args:
        import_id: Import ID
        db: Database session

    Returns:
        ImportStatusResponse: Import status and progress
    """
    imp = db.query(ImportHistory).filter(ImportHistory.import_id == import_id).first()

    if not imp:
        raise HTTPException(status_code=404, detail=f"Import {import_id} not found")

    # Determine status based on import data
    if imp.failed_rows == imp.total_rows:
        status = "failed"
        message = "Import failed - all rows had errors"
    elif imp.successful_rows + imp.failed_rows == imp.total_rows:
        status = "completed"
        message = f"Import completed - {imp.successful_rows}/{imp.total_rows} rows successful"
    else:
        status = "processing"
        message = f"Processing - {imp.successful_rows + imp.failed_rows}/{imp.total_rows} rows processed"

    # Calculate progress
    progress = ((imp.successful_rows + imp.failed_rows) / imp.total_rows * 100) if imp.total_rows > 0 else 0.0

    return ImportStatusResponse(
        import_id=imp.import_id,
        status=status,
        progress=progress,
        current_row=imp.successful_rows + imp.failed_rows,
        total_rows=imp.total_rows,
        successful_rows=imp.successful_rows,
        failed_rows=imp.failed_rows,
        message=message,
        started_at=imp.import_date,
        completed_at=imp.import_date if status == "completed" else None
    )


# ==================== Import Profile Endpoints ====================


@router.get("/import/profiles", response_model=ImportProfileListResponse)
async def list_import_profiles(
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    db: Session = Depends(get_db)
):
    """
    List all import profiles.

    Args:
        is_active: Optional filter by active status
        db: Database session

    Returns:
        ImportProfileListResponse: List of import profiles
    """
    service = ImportService(db)
    profiles = service.get_profiles(is_active=is_active)

    profile_responses = []
    for profile in profiles:
        profile_responses.append(ImportProfileResponse(
            profile_id=profile.profile_id,
            name=profile.name,
            account_id=profile.account_id,
            account_name=profile.account.account_name if profile.account else None,
            column_mappings=profile.column_mappings,
            date_format=profile.date_format,
            skip_rows=profile.skip_rows,
            is_active=profile.is_active,
            created_at=profile.created_at,
            updated_at=profile.updated_at
        ))

    return ImportProfileListResponse(
        profiles=profile_responses,
        total=len(profile_responses)
    )


@router.post("/import/profiles", response_model=ImportProfileResponse, status_code=201)
async def create_import_profile(
    profile: ImportProfileCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new import profile.

    Args:
        profile: Profile creation data
        db: Database session

    Returns:
        ImportProfileResponse: Created profile
    """
    service = ImportService(db)

    try:
        created = service.create_profile(
            name=profile.name,
            column_mappings=profile.column_mappings,
            account_id=profile.account_id,
            date_format=profile.date_format,
            skip_rows=profile.skip_rows
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return ImportProfileResponse(
        profile_id=created.profile_id,
        name=created.name,
        account_id=created.account_id,
        account_name=created.account.account_name if created.account else None,
        column_mappings=created.column_mappings,
        date_format=created.date_format,
        skip_rows=created.skip_rows,
        is_active=created.is_active,
        created_at=created.created_at,
        updated_at=created.updated_at
    )


@router.get("/import/profiles/{profile_id}", response_model=ImportProfileResponse)
async def get_import_profile(
    profile_id: int = PathParam(..., description="Profile ID"),
    db: Session = Depends(get_db)
):
    """
    Get a single import profile by ID.

    Args:
        profile_id: Profile ID
        db: Database session

    Returns:
        ImportProfileResponse: Profile details
    """
    service = ImportService(db)
    profile = service.get_profile(profile_id)

    if not profile:
        raise HTTPException(status_code=404, detail=f"Import profile {profile_id} not found")

    return ImportProfileResponse(
        profile_id=profile.profile_id,
        name=profile.name,
        account_id=profile.account_id,
        account_name=profile.account.account_name if profile.account else None,
        column_mappings=profile.column_mappings,
        date_format=profile.date_format,
        skip_rows=profile.skip_rows,
        is_active=profile.is_active,
        created_at=profile.created_at,
        updated_at=profile.updated_at
    )


@router.put("/import/profiles/{profile_id}", response_model=ImportProfileResponse)
async def update_import_profile(
    profile_id: int = PathParam(..., description="Profile ID"),
    profile: ImportProfileUpdate = None,
    db: Session = Depends(get_db)
):
    """
    Update an import profile.

    Args:
        profile_id: Profile ID
        profile: Profile update data
        db: Database session

    Returns:
        ImportProfileResponse: Updated profile
    """
    service = ImportService(db)

    # Build update kwargs from non-None fields
    update_data = {}
    if profile:
        if profile.name is not None:
            update_data['name'] = profile.name
        if profile.account_id is not None:
            update_data['account_id'] = profile.account_id
        if profile.column_mappings is not None:
            update_data['column_mappings'] = profile.column_mappings
        if profile.date_format is not None:
            update_data['date_format'] = profile.date_format
        if profile.skip_rows is not None:
            update_data['skip_rows'] = profile.skip_rows
        if profile.is_active is not None:
            update_data['is_active'] = profile.is_active

    try:
        updated = service.update_profile(profile_id, **update_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not updated:
        raise HTTPException(status_code=404, detail=f"Import profile {profile_id} not found")

    return ImportProfileResponse(
        profile_id=updated.profile_id,
        name=updated.name,
        account_id=updated.account_id,
        account_name=updated.account.account_name if updated.account else None,
        column_mappings=updated.column_mappings,
        date_format=updated.date_format,
        skip_rows=updated.skip_rows,
        is_active=updated.is_active,
        created_at=updated.created_at,
        updated_at=updated.updated_at
    )


@router.delete("/import/profiles/{profile_id}", status_code=204)
async def delete_import_profile(
    profile_id: int = PathParam(..., description="Profile ID"),
    db: Session = Depends(get_db)
):
    """
    Delete an import profile.

    Args:
        profile_id: Profile ID
        db: Database session
    """
    service = ImportService(db)
    deleted = service.delete_profile(profile_id)

    if not deleted:
        raise HTTPException(status_code=404, detail=f"Import profile {profile_id} not found")

    return None


@router.post("/import/profiles/suggest", response_model=List[ImportProfileSuggestion])
async def suggest_import_profiles(
    file: UploadFile = File(..., description="Excel file to analyze"),
    db: Session = Depends(get_db)
):
    """
    Suggest matching import profiles based on file columns.

    Analyzes the uploaded file's column headers and returns profiles
    that match, sorted by match score.

    Args:
        file: Uploaded Excel file
        db: Database session

    Returns:
        List of profile suggestions with match scores
    """
    import pandas as pd

    # Validate file type
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only .xlsx and .xls files are supported."
        )

    try:
        # Read just the header row
        contents = await file.read()
        import io
        df = pd.read_excel(io.BytesIO(contents), nrows=0)
        columns = list(df.columns)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to read file columns: {str(e)}"
        )

    service = ImportService(db)
    suggestions = service.suggest_profiles(columns)

    return [
        ImportProfileSuggestion(
            profile_id=s['profile_id'],
            name=s['name'],
            match_score=s['match_score'],
            matched_columns=s['matched_columns']
        )
        for s in suggestions
    ]
