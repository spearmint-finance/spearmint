"""Category API endpoints."""
"""
Category API endpoints.

Provides CRUD operations for categories and category rules.
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..schemas.category import (
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse,
    CategoryListResponse,
    CategoryRuleCreate,
    CategoryRuleUpdate,
    CategoryRuleResponse,
    CategoryRuleListResponse,
    TestCategoryRuleRequest,
    TestCategoryRuleResponse,
    ApplyCategoryRulesRequest,
    ApplyCategoryRulesResponse
)
from ..schemas.common import SuccessResponse
from ...services.category_service import CategoryService
from ...utils.validators import ValidationError

router = APIRouter()


@router.post("/categories", response_model=CategoryResponse, status_code=201)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new category.
    
    Args:
        category: Category data
        db: Database session
        
    Returns:
        CategoryResponse: Created category
    """
    service = CategoryService(db)
    
    try:
        created = service.create_category(
            category_name=category.category_name,
            category_type=category.category_type,
            parent_category_id=category.parent_category_id,
            description=category.description,
            entity_id=category.entity_id,
        )
        return created
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create category: {str(e)}")


@router.get("/categories/{category_id}", response_model=CategoryResponse)
def get_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    """
    Get category by ID.
    
    Args:
        category_id: Category ID
        db: Database session
        
    Returns:
        CategoryResponse: Category data
    """
    service = CategoryService(db)
    category = service.get_category(category_id)
    
    if not category:
        raise HTTPException(status_code=404, detail=f"Category {category_id} not found")
    
    return category


@router.get("/categories", response_model=CategoryListResponse)
def list_categories(
    category_type: Optional[str] = Query(None, pattern="^(Income|Expense|Transfer|Both)$", description="Category type filter"),
    parent_category_id: Optional[int] = Query(None, description="Parent category ID filter (null for root categories)"),
    include_transfer_categories: bool = Query(True, description="Include transfer categories"),
    search_text: Optional[str] = Query(None, description="Search in category name or description"),
    entity_id: Optional[int] = Query(None, description="Filter by entity ID (returns entity-specific + global categories)"),
    db: Session = Depends(get_db)
):
    """
    List categories with optional filters.
    
    Args:
        category_type: Category type filter
        parent_category_id: Parent category ID filter
        include_transfer_categories: Include transfer categories
        search_text: Search text
        db: Database session
        
    Returns:
        CategoryListResponse: List of categories
    """
    service = CategoryService(db)
    
    try:
        categories = service.list_categories(
            category_type=category_type,
            parent_category_id=parent_category_id,
            include_transfer_categories=include_transfer_categories,
            search_text=search_text,
            entity_id=entity_id,
        )

        # Get transaction counts per category in a single query
        from ...database.models import Transaction
        from sqlalchemy import func
        counts = dict(
            db.query(Transaction.category_id, func.count(Transaction.transaction_id))
            .group_by(Transaction.category_id)
            .all()
        )

        category_responses = []
        for cat in categories:
            resp = CategoryResponse.model_validate(cat)
            resp.transaction_count = counts.get(cat.category_id, 0)
            category_responses.append(resp)

        return CategoryListResponse(
            categories=category_responses,
            total=len(category_responses)
        )
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/categories/root", response_model=CategoryListResponse)
def get_root_categories(
    category_type: Optional[str] = Query(None, pattern="^(Income|Expense|Transfer|Both)$", description="Category type filter"),
    db: Session = Depends(get_db)
):
    """
    Get root categories (categories without parent).
    
    Args:
        category_type: Category type filter
        db: Database session
        
    Returns:
        CategoryListResponse: List of root categories
    """
    service = CategoryService(db)
    
    categories = service.get_root_categories(category_type=category_type)
    
    return CategoryListResponse(
        categories=categories,
        total=len(categories)
    )


@router.get("/categories/{category_id}/children", response_model=CategoryListResponse)
def get_child_categories(
    category_id: int,
    db: Session = Depends(get_db)
):
    """
    Get child categories of a parent category.
    
    Args:
        category_id: Parent category ID
        db: Database session
        
    Returns:
        CategoryListResponse: List of child categories
    """
    service = CategoryService(db)
    
    # Verify parent exists
    parent = service.get_category(category_id)
    if not parent:
        raise HTTPException(status_code=404, detail=f"Category {category_id} not found")
    
    categories = service.get_child_categories(category_id)
    
    return CategoryListResponse(
        categories=categories,
        total=len(categories)
    )


@router.put("/categories/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category: CategoryUpdate,
    db: Session = Depends(get_db)
):
    """
    Update category.
    
    Args:
        category_id: Category ID
        category: Updated category data
        db: Database session
        
    Returns:
        CategoryResponse: Updated category
    """
    service = CategoryService(db)
    
    try:
        # Convert to dict and remove None values
        updates = category.model_dump(exclude_unset=True)
        
        updated = service.update_category(category_id, **updates)
        
        if not updated:
            raise HTTPException(status_code=404, detail=f"Category {category_id} not found")
        
        return updated
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update category: {str(e)}")


@router.delete("/categories/{category_id}", response_model=SuccessResponse)
def delete_category(
    category_id: int,
    force: bool = Query(False, description="Force delete even if category has transactions or children"),
    db: Session = Depends(get_db)
):
    """
    Delete category.
    
    Args:
        category_id: Category ID
        force: Force delete
        db: Database session
        
    Returns:
        SuccessResponse: Success message
    """
    service = CategoryService(db)
    
    try:
        deleted = service.delete_category(category_id, force=force)
        
        if not deleted:
            raise HTTPException(status_code=404, detail=f"Category {category_id} not found")
        
        return SuccessResponse(message=f"Category {category_id} deleted successfully")
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete category: {str(e)}")


@router.put("/categories/{category_id}/merge")
def merge_category(
    category_id: int,
    body: dict,
    db: Session = Depends(get_db)
):
    """
    Merge source category into target category. All transactions, splits,
    rules, budgets, and child categories are reassigned to the target.
    The source category is then deleted.

    Body: { "target_category_id": 123 }
    """
    service = CategoryService(db)
    target_id = body.get("target_category_id")
    if not target_id:
        raise HTTPException(status_code=400, detail="target_category_id is required")

    try:
        result = service.merge_category(category_id, target_id)
        return {
            "message": f"Category {category_id} merged into {target_id}",
            **result,
        }
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to merge category: {str(e)}")


# ============================================================================
# Category Rule Endpoints
# ============================================================================

@router.get("/category-rules", response_model=CategoryRuleListResponse)
def list_category_rules(
    active_only: bool = Query(False, description="Only return active rules"),
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    db: Session = Depends(get_db)
):
    """
    List all category rules.

    Args:
        active_only: Only return active rules
        category_id: Filter by category
        db: Database session

    Returns:
        CategoryRuleListResponse: List of category rules
    """
    service = CategoryService(db)
    rules = service.list_category_rules(active_only=active_only, category_id=category_id)

    return CategoryRuleListResponse(
        rules=rules,
        total=len(rules)
    )


@router.get("/category-rules/{rule_id}", response_model=CategoryRuleResponse)
def get_category_rule(
    rule_id: int,
    db: Session = Depends(get_db)
):
    """
    Get category rule by ID.

    Args:
        rule_id: Rule ID
        db: Database session

    Returns:
        CategoryRuleResponse: Category rule data
    """
    service = CategoryService(db)
    rule = service.get_category_rule(rule_id)

    if not rule:
        raise HTTPException(status_code=404, detail=f"Category rule {rule_id} not found")

    return rule


@router.post("/category-rules", response_model=CategoryRuleResponse, status_code=201)
def create_category_rule(
    rule: CategoryRuleCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new category rule.

    Args:
        rule: Category rule data
        db: Database session

    Returns:
        CategoryRuleResponse: Created category rule
    """
    service = CategoryService(db)

    try:
        created = service.create_category_rule(
            rule_name=rule.rule_name,
            category_id=rule.category_id,
            rule_priority=rule.rule_priority,
            is_active=rule.is_active,
            description_pattern=rule.description_pattern,
            source_pattern=rule.source_pattern,
            amount_min=rule.amount_min,
            amount_max=rule.amount_max,
            payment_method_pattern=rule.payment_method_pattern,
            transaction_type_pattern=rule.transaction_type_pattern
        )
        return created
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create category rule: {str(e)}")


@router.put("/category-rules/{rule_id}", response_model=CategoryRuleResponse)
def update_category_rule(
    rule_id: int,
    rule: CategoryRuleUpdate,
    db: Session = Depends(get_db)
):
    """
    Update category rule.

    Args:
        rule_id: Rule ID
        rule: Updated rule data
        db: Database session

    Returns:
        CategoryRuleResponse: Updated category rule
    """
    service = CategoryService(db)

    try:
        updates = rule.model_dump(exclude_unset=True)
        updated = service.update_category_rule(rule_id, **updates)

        if not updated:
            raise HTTPException(status_code=404, detail=f"Category rule {rule_id} not found")

        return updated
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update category rule: {str(e)}")


@router.delete("/category-rules/{rule_id}", response_model=SuccessResponse)
def delete_category_rule(
    rule_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete category rule.

    Args:
        rule_id: Rule ID
        db: Database session

    Returns:
        SuccessResponse: Success message
    """
    service = CategoryService(db)

    try:
        deleted = service.delete_category_rule(rule_id)

        if not deleted:
            raise HTTPException(status_code=404, detail=f"Category rule {rule_id} not found")

        return SuccessResponse(message=f"Category rule {rule_id} deleted successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete category rule: {str(e)}")


@router.post("/category-rules/test", response_model=TestCategoryRuleResponse)
def test_category_rule(
    request: TestCategoryRuleRequest,
    db: Session = Depends(get_db)
):
    """
    Test a category rule against existing transactions.

    Args:
        request: Test rule request
        db: Database session

    Returns:
        TestCategoryRuleResponse: Test results
    """
    service = CategoryService(db)

    try:
        result = service.test_category_rule(
            description_pattern=request.description_pattern,
            source_pattern=request.source_pattern,
            amount_min=request.amount_min,
            amount_max=request.amount_max,
            payment_method_pattern=request.payment_method_pattern,
            transaction_type_pattern=request.transaction_type_pattern,
            limit=request.limit
        )

        # Convert transactions to dict for response
        sample_transactions = [
            {
                'transaction_id': tx.transaction_id,
                'transaction_date': tx.transaction_date.isoformat(),
                'amount': float(tx.amount),
                'transaction_type': tx.transaction_type,
                'description': tx.description,
                'source': tx.source,
                'payment_method': tx.payment_method,
                'category_name': tx.category.category_name if tx.category else None
            }
            for tx in result['sample_transactions']
        ]

        return TestCategoryRuleResponse(
            total_matches=result['total_matches'],
            sample_transactions=sample_transactions,
            has_more=result['has_more']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to test category rule: {str(e)}")


@router.post("/category-rules/apply", response_model=ApplyCategoryRulesResponse)
def apply_category_rules(
    request: ApplyCategoryRulesRequest,
    db: Session = Depends(get_db)
):
    """
    Apply category rules to transactions.

    Args:
        request: Apply rules request
        db: Database session

    Returns:
        ApplyCategoryRulesResponse: Application results
    """
    service = CategoryService(db)

    try:
        result = service.apply_category_rules(
            transaction_ids=request.transaction_ids,
            rule_ids=request.rule_ids,
            force_recategorize=request.force_recategorize
        )

        return ApplyCategoryRulesResponse(
            total_processed=result['total_processed'],
            categorized_count=result['categorized_count'],
            skipped_count=result['skipped_count'],
            rules_applied=result['rules_applied']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to apply category rules: {str(e)}")

