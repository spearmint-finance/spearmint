"""Import Pydantic schemas."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class ImportRequest(BaseModel):
    """Schema for import request."""
    
    mode: str = Field(default="incremental", pattern="^(full|incremental|update)$", description="Import mode")
    skip_duplicates: bool = Field(default=True, description="Skip duplicate transactions")


class ImportErrorDetail(BaseModel):
    """Schema for import error detail."""
    
    row: int = Field(..., description="Row number")
    field: str = Field(..., description="Field name")
    message: str = Field(..., description="Error message")
    value: Optional[Any] = Field(None, description="Invalid value")


class ImportResponse(BaseModel):
    """Schema for import response."""
    
    total_rows: int = Field(..., description="Total rows processed")
    successful_rows: int = Field(..., description="Successfully imported rows")
    failed_rows: int = Field(..., description="Failed rows")
    classified_rows: int = Field(..., description="Automatically classified rows")
    skipped_duplicates: int = Field(..., description="Skipped duplicate rows")
    success_rate: float = Field(..., description="Success rate percentage")
    errors: List[ImportErrorDetail] = Field(default_factory=list, description="List of errors")
    warnings: List[str] = Field(default_factory=list, description="List of warnings")


class ImportHistoryItem(BaseModel):
    """Schema for a single import history item."""

    import_id: int = Field(..., description="Import ID")
    import_date: datetime = Field(..., description="Import date")
    file_name: str = Field(..., description="File name")
    total_rows: int = Field(..., description="Total rows")
    successful_rows: int = Field(..., description="Successful rows")
    failed_rows: int = Field(..., description="Failed rows")
    classified_rows: int = Field(..., description="Classified rows")
    import_mode: str = Field(..., description="Import mode")
    success_rate: float = Field(..., description="Success rate percentage")


class ImportHistoryResponse(BaseModel):
    """Schema for import history list response."""

    imports: List[ImportHistoryItem] = Field(..., description="List of imports")
    total: int = Field(..., description="Total number of imports")


class ImportHistoryDetailResponse(BaseModel):
    """Schema for detailed import history response."""

    import_id: int = Field(..., description="Import ID")
    import_date: datetime = Field(..., description="Import date")
    file_name: str = Field(..., description="File name")
    file_path: str = Field(..., description="File path")
    total_rows: int = Field(..., description="Total rows")
    successful_rows: int = Field(..., description="Successful rows")
    failed_rows: int = Field(..., description="Failed rows")
    classified_rows: int = Field(..., description="Classified rows")
    import_mode: str = Field(..., description="Import mode")
    error_log: Optional[str] = Field(None, description="Error log")
    success_rate: float = Field(..., description="Success rate percentage")


class ImportStatusResponse(BaseModel):
    """Schema for import status response."""

    import_id: int = Field(..., description="Import ID")
    status: str = Field(..., description="Import status (pending, processing, completed, failed)")
    progress: float = Field(..., description="Progress percentage (0-100)")
    current_row: int = Field(..., description="Current row being processed")
    total_rows: int = Field(..., description="Total rows to process")
    successful_rows: int = Field(..., description="Successfully processed rows")
    failed_rows: int = Field(..., description="Failed rows")
    message: Optional[str] = Field(None, description="Status message")
    started_at: Optional[datetime] = Field(None, description="Processing start time")
    completed_at: Optional[datetime] = Field(None, description="Processing completion time")

