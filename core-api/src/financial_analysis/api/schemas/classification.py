"""
Pydantic schemas for classification endpoints.
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class ClassificationBase(BaseModel):
    """Base classification schema."""
    classification_name: str = Field(..., description="Name of the classification")
    classification_code: str = Field(..., description="Unique code for the classification")
    description: Optional[str] = Field(None, description="Description of the classification")
    exclude_from_income_calc: bool = Field(False, description="Exclude from income calculations")
    exclude_from_expense_calc: bool = Field(False, description="Exclude from expense calculations")
    exclude_from_cashflow_calc: bool = Field(False, description="Exclude from cash flow calculations")


class ClassificationCreate(ClassificationBase):
    """Schema for creating a new classification."""
    pass


class ClassificationUpdate(BaseModel):
    """Schema for updating a classification."""
    classification_name: Optional[str] = Field(None, description="Name of the classification")
    description: Optional[str] = Field(None, description="Description of the classification")
    exclude_from_income_calc: Optional[bool] = Field(None, description="Exclude from income calculations")
    exclude_from_expense_calc: Optional[bool] = Field(None, description="Exclude from expense calculations")
    exclude_from_cashflow_calc: Optional[bool] = Field(None, description="Exclude from cash flow calculations")


class ClassificationResponse(ClassificationBase):
    """Schema for classification response."""
    classification_id: int = Field(..., description="Classification ID")
    is_system_classification: bool = Field(..., description="Whether this is a system classification")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "classification_id": 1,
                "classification_name": "Standard Transaction",
                "classification_code": "STANDARD",
                "description": "Regular income or expense transaction",
                "exclude_from_income_calc": False,
                "exclude_from_expense_calc": False,
                "exclude_from_cashflow_calc": False,
                "is_system_classification": True,
                "created_at": "2025-01-01T00:00:00",
                "updated_at": "2025-01-01T00:00:00"
            }
        }


class ClassificationListResponse(BaseModel):
    """Schema for list of classifications."""
    classifications: List[ClassificationResponse] = Field(..., description="List of classifications")
    total: int = Field(..., description="Total number of classifications")
    
    class Config:
        json_schema_extra = {
            "example": {
                "classifications": [
                    {
                        "classification_id": 1,
                        "classification_name": "Standard Transaction",
                        "classification_code": "STANDARD",
                        "description": "Regular income or expense transaction",
                        "exclude_from_income_calc": False,
                        "exclude_from_expense_calc": False,
                        "exclude_from_cashflow_calc": False,
                        "is_system_classification": True,
                        "created_at": "2025-01-01T00:00:00",
                        "updated_at": "2025-01-01T00:00:00"
                    }
                ],
                "total": 10
            }
        }


class ClassifyTransactionRequest(BaseModel):
    """Schema for classifying a transaction."""
    classification_id: int = Field(..., description="Classification ID to apply")
    
    class Config:
        json_schema_extra = {
            "example": {
                "classification_id": 2
            }
        }


class BulkClassifyRequest(BaseModel):
    """Schema for bulk classification."""
    transaction_ids: List[int] = Field(..., description="List of transaction IDs to classify")
    classification_id: int = Field(..., description="Classification ID to apply")
    
    class Config:
        json_schema_extra = {
            "example": {
                "transaction_ids": [1, 2, 3, 4, 5],
                "classification_id": 2
            }
        }


class BulkClassifyResponse(BaseModel):
    """Schema for bulk classification response."""
    success_count: int = Field(..., description="Number of successfully classified transactions")
    failed_count: int = Field(..., description="Number of failed classifications")
    failed_ids: List[int] = Field(default_factory=list, description="IDs of transactions that failed")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success_count": 5,
                "failed_count": 0,
                "failed_ids": []
            }
        }


class AutoClassifyRequest(BaseModel):
    """Schema for auto-classification request."""
    transaction_ids: Optional[List[int]] = Field(None, description="Specific transaction IDs (optional, defaults to all unclassified)")
    force_reclassify: bool = Field(False, description="Force reclassification of already classified transactions")
    
    class Config:
        json_schema_extra = {
            "example": {
                "transaction_ids": None,
                "force_reclassify": False
            }
        }


class AutoClassifyResponse(BaseModel):
    """Schema for auto-classification response."""
    total_processed: int = Field(..., description="Total transactions processed")
    classified_count: int = Field(..., description="Number of transactions classified")
    skipped_count: int = Field(..., description="Number of transactions skipped")
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_processed": 100,
                "classified_count": 85,
                "skipped_count": 15
            }
        }


class ClassificationRuleBase(BaseModel):
    """Base classification rule schema."""
    rule_name: str = Field(..., description="Name of the rule")
    rule_priority: int = Field(100, description="Rule priority (lower = higher priority)")
    classification_id: int = Field(..., description="Classification to apply")
    is_active: bool = Field(True, description="Whether the rule is active")
    description_pattern: Optional[str] = Field(None, description="Pattern to match in description")
    category_pattern: Optional[str] = Field(None, description="Pattern to match in category")
    source_pattern: Optional[str] = Field(None, description="Pattern to match in source")
    amount_min: Optional[float] = Field(None, description="Minimum amount")
    amount_max: Optional[float] = Field(None, description="Maximum amount")
    payment_method_pattern: Optional[str] = Field(None, description="Pattern to match in payment method")


class ClassificationRuleCreate(ClassificationRuleBase):
    """Schema for creating a classification rule."""
    pass


class ClassificationRuleUpdate(BaseModel):
    """Schema for updating a classification rule."""
    rule_name: Optional[str] = Field(None, description="Name of the rule")
    rule_priority: Optional[int] = Field(None, description="Rule priority")
    classification_id: Optional[int] = Field(None, description="Classification to apply")
    is_active: Optional[bool] = Field(None, description="Whether the rule is active")
    description_pattern: Optional[str] = Field(None, description="Pattern to match in description")
    category_pattern: Optional[str] = Field(None, description="Pattern to match in category")
    source_pattern: Optional[str] = Field(None, description="Pattern to match in source")
    amount_min: Optional[float] = Field(None, description="Minimum amount")
    amount_max: Optional[float] = Field(None, description="Maximum amount")
    payment_method_pattern: Optional[str] = Field(None, description="Pattern to match in payment method")


class ClassificationRuleResponse(ClassificationRuleBase):
    """Schema for classification rule response."""
    rule_id: int = Field(..., description="Rule ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "rule_id": 1,
                "rule_name": "Credit Card Payment Detection",
                "rule_priority": 10,
                "classification_id": 3,
                "is_active": True,
                "description_pattern": "%credit card payment%",
                "category_pattern": None,
                "source_pattern": None,
                "amount_min": None,
                "amount_max": None,
                "payment_method_pattern": None,
                "created_at": "2025-01-01T00:00:00",
                "updated_at": "2025-01-01T00:00:00"
            }
        }


class ClassificationRuleListResponse(BaseModel):
    """Schema for list of classification rules."""
    rules: List[ClassificationRuleResponse] = Field(..., description="List of classification rules")
    total: int = Field(..., description="Total number of rules")
    
    class Config:
        json_schema_extra = {
            "example": {
                "rules": [
                    {
                        "rule_id": 1,
                        "rule_name": "Credit Card Payment Detection",
                        "rule_priority": 10,
                        "classification_id": 3,
                        "is_active": True,
                        "description_pattern": "%credit card payment%",
                        "category_pattern": None,
                        "source_pattern": None,
                        "amount_min": None,
                        "amount_max": None,
                        "payment_method_pattern": None,
                        "created_at": "2025-01-01T00:00:00",
                        "updated_at": "2025-01-01T00:00:00"
                    }
                ],
                "total": 3
            }
        }


class TestRuleRequest(BaseModel):
    """Schema for testing a classification rule."""
    description_pattern: Optional[str] = Field(None, description="Pattern to match in description")
    category_pattern: Optional[str] = Field(None, description="Pattern to match in category")
    source_pattern: Optional[str] = Field(None, description="Pattern to match in source")
    amount_min: Optional[float] = Field(None, description="Minimum amount")
    amount_max: Optional[float] = Field(None, description="Maximum amount")
    payment_method_pattern: Optional[str] = Field(None, description="Pattern to match in payment method")


class TestRuleResponse(BaseModel):
    """Schema for rule test response."""
    matching_transactions: int = Field(..., description="Number of transactions that would match")
    sample_transaction_ids: List[int] = Field(..., description="Sample transaction IDs (max 10)")

    class Config:
        json_schema_extra = {
            "example": {
                "matching_transactions": 25,
                "sample_transaction_ids": [1, 5, 12, 18, 23]
            }
        }


class ApplyRulesRequest(BaseModel):
    """Schema for applying classification rules."""
    dry_run: bool = Field(True, description="If true, only preview changes without applying them")
    rule_ids: Optional[List[int]] = Field(None, description="Specific rule IDs to apply (optional, defaults to all active rules)")

    class Config:
        json_schema_extra = {
            "example": {
                "dry_run": False,
                "rule_ids": None
            }
        }


class ApplyRulesResponse(BaseModel):
    """Schema for apply rules response."""
    dry_run: bool = Field(..., description="Whether this was a dry run")
    total_rules_processed: int = Field(..., description="Number of rules processed")
    total_transactions_updated: int = Field(..., description="Total transactions updated/would be updated")
    rules_applied: List[dict] = Field(..., description="Details of each rule application")

    class Config:
        json_schema_extra = {
            "example": {
                "dry_run": False,
                "total_rules_processed": 3,
                "total_transactions_updated": 42,
                "rules_applied": [
                    {
                        "rule_id": 1,
                        "rule_name": "Capital Expense - 100 S Stratford",
                        "classification_name": "Capital Expense",
                        "transactions_matched": 42
                    }
                ]
            }
        }

