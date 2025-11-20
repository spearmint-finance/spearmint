"""Category Pydantic schemas."""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class CategoryBase(BaseModel):
    """Base category schema with common fields."""
    
    category_name: str = Field(..., min_length=1, max_length=100, description="Category name")
    category_type: str = Field(..., pattern="^(Income|Expense|Both)$", description="Category type")
    parent_category_id: Optional[int] = Field(None, gt=0, description="Parent category ID")
    description: Optional[str] = Field(None, description="Category description")
    is_transfer_category: bool = Field(default=False, description="Is transfer category")


class CategoryCreate(CategoryBase):
    """Schema for creating a category."""
    pass


class CategoryUpdate(BaseModel):
    """Schema for updating a category."""
    
    category_name: Optional[str] = Field(None, min_length=1, max_length=100, description="Category name")
    category_type: Optional[str] = Field(None, pattern="^(Income|Expense|Both)$", description="Category type")
    parent_category_id: Optional[int] = Field(None, gt=0, description="Parent category ID")
    description: Optional[str] = Field(None, description="Category description")
    is_transfer_category: Optional[bool] = Field(None, description="Is transfer category")


class CategoryResponse(CategoryBase):
    """Schema for category response."""
    
    category_id: int = Field(..., description="Category ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    
    model_config = ConfigDict(from_attributes=True)


class CategoryListResponse(BaseModel):
    """Schema for category list response."""

    categories: List[CategoryResponse] = Field(..., description="List of categories")
    total: int = Field(..., description="Total number of categories")


# ============================================================================
# Category Rule Schemas
# ============================================================================

class CategoryRuleBase(BaseModel):
    """Base category rule schema."""

    rule_name: str = Field(..., min_length=1, max_length=100, description="Name of the rule")
    rule_priority: int = Field(100, ge=1, description="Rule priority (lower = higher priority)")
    category_id: int = Field(..., gt=0, description="Category to assign when rule matches")
    is_active: bool = Field(True, description="Whether the rule is active")
    description_pattern: Optional[str] = Field(None, max_length=255, description="Pattern to match in description (SQL LIKE syntax with %)")
    source_pattern: Optional[str] = Field(None, max_length=255, description="Pattern to match in source")
    amount_min: Optional[float] = Field(None, description="Minimum amount")
    amount_max: Optional[float] = Field(None, description="Maximum amount")
    payment_method_pattern: Optional[str] = Field(None, max_length=50, description="Pattern to match in payment method")
    transaction_type_pattern: Optional[str] = Field(None, pattern="^(Income|Expense)$", description="Transaction type to match")


class CategoryRuleCreate(CategoryRuleBase):
    """Schema for creating a category rule."""
    pass


class CategoryRuleUpdate(BaseModel):
    """Schema for updating a category rule."""

    rule_name: Optional[str] = Field(None, min_length=1, max_length=100, description="Name of the rule")
    rule_priority: Optional[int] = Field(None, ge=1, description="Rule priority (lower = higher priority)")
    category_id: Optional[int] = Field(None, gt=0, description="Category to assign when rule matches")
    is_active: Optional[bool] = Field(None, description="Whether the rule is active")
    description_pattern: Optional[str] = Field(None, max_length=255, description="Pattern to match in description")
    source_pattern: Optional[str] = Field(None, max_length=255, description="Pattern to match in source")
    amount_min: Optional[float] = Field(None, description="Minimum amount")
    amount_max: Optional[float] = Field(None, description="Maximum amount")
    payment_method_pattern: Optional[str] = Field(None, max_length=50, description="Pattern to match in payment method")
    transaction_type_pattern: Optional[str] = Field(None, pattern="^(Income|Expense)$", description="Transaction type to match")


class CategoryRuleResponse(CategoryRuleBase):
    """Schema for category rule response."""

    rule_id: int = Field(..., description="Rule ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = ConfigDict(from_attributes=True)


class CategoryRuleListResponse(BaseModel):
    """Schema for category rule list response."""

    rules: List[CategoryRuleResponse] = Field(..., description="List of category rules")
    total: int = Field(..., description="Total number of rules")


class TestCategoryRuleRequest(BaseModel):
    """Schema for testing a category rule."""

    description_pattern: Optional[str] = Field(None, max_length=255, description="Pattern to match in description")
    source_pattern: Optional[str] = Field(None, max_length=255, description="Pattern to match in source")
    amount_min: Optional[float] = Field(None, description="Minimum amount")
    amount_max: Optional[float] = Field(None, description="Maximum amount")
    payment_method_pattern: Optional[str] = Field(None, max_length=50, description="Pattern to match in payment method")
    transaction_type_pattern: Optional[str] = Field(None, pattern="^(Income|Expense)$", description="Transaction type to match")
    limit: int = Field(10, ge=1, le=100, description="Maximum number of matching transactions to return")


class TestCategoryRuleResponse(BaseModel):
    """Schema for test category rule response."""

    total_matches: int = Field(..., description="Total number of matching transactions")
    sample_transactions: List[dict] = Field(..., description="Sample matching transactions")
    has_more: bool = Field(..., description="Whether there are more matches beyond the limit")


class ApplyCategoryRulesRequest(BaseModel):
    """Schema for applying category rules."""

    transaction_ids: Optional[List[int]] = Field(None, description="Specific transaction IDs to process (None = all)")
    rule_ids: Optional[List[int]] = Field(None, description="Specific rule IDs to apply (None = all active rules)")
    force_recategorize: bool = Field(False, description="If True, recategorize even if already categorized")


class ApplyCategoryRulesResponse(BaseModel):
    """Schema for apply category rules response."""

    total_processed: int = Field(..., description="Total number of transactions processed")
    categorized_count: int = Field(..., description="Number of transactions categorized")
    skipped_count: int = Field(..., description="Number of transactions skipped")
    rules_applied: int = Field(..., description="Number of rules applied")

