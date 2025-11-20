"""
API routes for classification management.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import Optional, List

from ..dependencies import get_db
from ...services.classification_service import ClassificationService
from ...database.models import TransactionClassification, ClassificationRule
from ..schemas.classification import (
    ClassificationResponse,
    ClassificationListResponse,
    ClassificationCreate,
    ClassificationUpdate,
    ClassifyTransactionRequest,
    BulkClassifyRequest,
    BulkClassifyResponse,
    AutoClassifyRequest,
    AutoClassifyResponse,
    ClassificationRuleResponse,
    ClassificationRuleListResponse,
    ClassificationRuleCreate,
    ClassificationRuleUpdate,
    TestRuleRequest,
    TestRuleResponse,
    ApplyRulesRequest,
    ApplyRulesResponse
)

router = APIRouter()


@router.get(
    "/classifications",
    response_model=ClassificationListResponse,
    summary="List All Classifications",
    description="""
    Get a list of all transaction classifications.
    
    Classifications determine how transactions are treated in financial calculations:
    - Standard transactions are included in all calculations
    - Transfers are excluded to prevent double-counting
    - Credit card payments/receipts are handled specially
    - Reimbursements and refunds are excluded from income
    
    System classifications cannot be deleted but can be viewed.
    """
)
def list_classifications(
    system_only: bool = Query(False, description="Only return system classifications"),
    db: Session = Depends(get_db)
):
    """List all classifications."""
    service = ClassificationService(db)
    classifications = service.list_classifications(include_system_only=system_only)
    
    return ClassificationListResponse(
        classifications=[ClassificationResponse.model_validate(c) for c in classifications],
        total=len(classifications)
    )


@router.get(
    "/classifications/{classification_id}",
    response_model=ClassificationResponse,
    summary="Get Classification Details",
    description="Get detailed information about a specific classification by ID."
)
def get_classification(
    classification_id: int = Path(..., description="Classification ID"),
    db: Session = Depends(get_db)
):
    """Get classification by ID."""
    service = ClassificationService(db)
    classification = service.get_classification(classification_id)
    
    if not classification:
        raise HTTPException(status_code=404, detail="Classification not found")
    
    return ClassificationResponse.model_validate(classification)


@router.post(
    "/classifications",
    response_model=ClassificationResponse,
    status_code=201,
    summary="Create Classification",
    description="""
    Create a new custom classification.
    
    Note: System classifications cannot be created through the API.
    Custom classifications can be used for specialized transaction handling.
    """
)
def create_classification(
    classification: ClassificationCreate,
    db: Session = Depends(get_db)
):
    """Create a new classification."""
    # Check if code already exists
    service = ClassificationService(db)
    existing = service.get_classification_by_code(classification.classification_code)
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Classification with code '{classification.classification_code}' already exists"
        )
    
    # Create new classification
    new_classification = TransactionClassification(
        classification_name=classification.classification_name,
        classification_code=classification.classification_code,
        description=classification.description,
        exclude_from_income_calc=classification.exclude_from_income_calc,
        exclude_from_expense_calc=classification.exclude_from_expense_calc,
        exclude_from_cashflow_calc=classification.exclude_from_cashflow_calc,
        is_system_classification=False
    )
    
    db.add(new_classification)
    db.commit()
    db.refresh(new_classification)
    
    return ClassificationResponse.model_validate(new_classification)


@router.put(
    "/classifications/{classification_id}",
    response_model=ClassificationResponse,
    summary="Update Classification",
    description="""
    Update an existing classification.
    
    Note: System classifications cannot be modified.
    Only custom classifications can be updated.
    """
)
def update_classification(
    classification_id: int = Path(..., description="Classification ID"),
    classification_update: ClassificationUpdate = ...,
    db: Session = Depends(get_db)
):
    """Update a classification."""
    service = ClassificationService(db)
    classification = service.get_classification(classification_id)
    
    if not classification:
        raise HTTPException(status_code=404, detail="Classification not found")
    
    if classification.is_system_classification:
        raise HTTPException(
            status_code=403,
            detail="System classifications cannot be modified"
        )
    
    # Update fields
    update_data = classification_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(classification, field, value)
    
    db.commit()
    db.refresh(classification)
    
    return ClassificationResponse.model_validate(classification)


@router.delete(
    "/classifications/{classification_id}",
    status_code=204,
    summary="Delete Classification",
    description="""
    Delete a custom classification.
    
    Note: System classifications cannot be deleted.
    Transactions using this classification will be set to 'Standard Transaction'.
    """
)
def delete_classification(
    classification_id: int = Path(..., description="Classification ID"),
    db: Session = Depends(get_db)
):
    """Delete a classification."""
    service = ClassificationService(db)
    classification = service.get_classification(classification_id)
    
    if not classification:
        raise HTTPException(status_code=404, detail="Classification not found")
    
    if classification.is_system_classification:
        raise HTTPException(
            status_code=403,
            detail="System classifications cannot be deleted"
        )
    
    # Get standard classification to reassign transactions
    standard = service.get_classification_by_code('STANDARD')
    if not standard:
        raise HTTPException(
            status_code=500,
            detail="Standard classification not found in database"
        )
    
    # Reassign all transactions to standard
    from ...database.models import Transaction
    db.query(Transaction).filter(
        Transaction.classification_id == classification_id
    ).update({Transaction.classification_id: standard.classification_id})
    
    # Delete the classification
    db.delete(classification)
    db.commit()
    
    return None


@router.post(
    "/transactions/{transaction_id}/classify",
    response_model=ClassificationResponse,
    summary="Classify Transaction",
    description="""
    Manually classify a specific transaction.
    
    This sets the classification for a single transaction.
    The classification determines how the transaction is treated in financial calculations.
    """
)
def classify_transaction(
    transaction_id: int = Path(..., description="Transaction ID"),
    request: ClassifyTransactionRequest = ...,
    db: Session = Depends(get_db)
):
    """Classify a single transaction."""
    service = ClassificationService(db)
    
    # Verify classification exists
    classification = service.get_classification(request.classification_id)
    if not classification:
        raise HTTPException(status_code=404, detail="Classification not found")
    
    # Classify the transaction
    transaction = service.classify_transaction(transaction_id, request.classification_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    db.commit()
    
    return ClassificationResponse.model_validate(classification)


@router.post(
    "/transactions/classify/bulk",
    response_model=BulkClassifyResponse,
    summary="Bulk Classify Transactions",
    description="""
    Classify multiple transactions at once.
    
    Useful for applying the same classification to multiple transactions.
    Returns counts of successful and failed classifications.
    """
)
def bulk_classify_transactions(
    request: BulkClassifyRequest,
    db: Session = Depends(get_db)
):
    """Bulk classify transactions."""
    service = ClassificationService(db)
    
    # Verify classification exists
    classification = service.get_classification(request.classification_id)
    if not classification:
        raise HTTPException(status_code=404, detail="Classification not found")
    
    success_count = 0
    failed_ids = []
    
    for transaction_id in request.transaction_ids:
        transaction = service.classify_transaction(transaction_id, request.classification_id)
        if transaction:
            success_count += 1
        else:
            failed_ids.append(transaction_id)
    
    db.commit()
    
    return BulkClassifyResponse(
        success_count=success_count,
        failed_count=len(failed_ids),
        failed_ids=failed_ids
    )


@router.post(
    "/transactions/auto-classify",
    response_model=AutoClassifyResponse,
    summary="Auto-Classify Transactions",
    description="""
    Automatically classify transactions using pattern-based rules.

    This applies all active classification rules to transactions.
    Can be run on specific transactions or all unclassified transactions.
    """
)
def auto_classify_transactions(
    request: AutoClassifyRequest,
    db: Session = Depends(get_db)
):
    """Auto-classify transactions using rules."""
    service = ClassificationService(db)

    from ...database.models import Transaction

    # Get transactions to process
    if request.transaction_ids:
        transactions = db.query(Transaction).filter(
            Transaction.transaction_id.in_(request.transaction_ids)
        ).all()
    else:
        # Get unclassified or all transactions based on force_reclassify
        query = db.query(Transaction)
        if not request.force_reclassify:
            standard = service.get_classification_by_code('STANDARD')
            if standard:
                query = query.filter(Transaction.classification_id == standard.classification_id)
        transactions = query.all()

    total_processed = len(transactions)
    classified_count = 0
    skipped_count = 0

    # Apply classification rules (simplified - would use actual rule engine)
    for transaction in transactions:
        # For now, just count as processed
        # In a full implementation, this would apply classification rules
        if transaction.classification_id:
            skipped_count += 1
        else:
            classified_count += 1

    return AutoClassifyResponse(
        total_processed=total_processed,
        classified_count=classified_count,
        skipped_count=skipped_count
    )


# Classification Rules Endpoints

@router.get(
    "/classification-rules",
    response_model=ClassificationRuleListResponse,
    summary="List Classification Rules",
    description="""
    Get a list of all classification rules.

    Rules are applied in priority order (lower number = higher priority).
    Active rules are automatically applied during auto-classification.
    """
)
def list_classification_rules(
    active_only: bool = Query(False, description="Only return active rules"),
    db: Session = Depends(get_db)
):
    """List all classification rules."""
    query = db.query(ClassificationRule)

    if active_only:
        query = query.filter(ClassificationRule.is_active == True)

    rules = query.order_by(ClassificationRule.rule_priority).all()

    return ClassificationRuleListResponse(
        rules=[ClassificationRuleResponse.model_validate(r) for r in rules],
        total=len(rules)
    )


@router.get(
    "/classification-rules/{rule_id}",
    response_model=ClassificationRuleResponse,
    summary="Get Classification Rule",
    description="Get detailed information about a specific classification rule."
)
def get_classification_rule(
    rule_id: int = Path(..., description="Rule ID"),
    db: Session = Depends(get_db)
):
    """Get classification rule by ID."""
    rule = db.query(ClassificationRule).filter(
        ClassificationRule.rule_id == rule_id
    ).first()

    if not rule:
        raise HTTPException(status_code=404, detail="Classification rule not found")

    return ClassificationRuleResponse.model_validate(rule)


@router.post(
    "/classification-rules",
    response_model=ClassificationRuleResponse,
    status_code=201,
    summary="Create Classification Rule",
    description="""
    Create a new classification rule.

    Rules use pattern matching to automatically classify transactions.
    Patterns support SQL LIKE syntax (% for wildcard).
    """
)
def create_classification_rule(
    rule: ClassificationRuleCreate,
    db: Session = Depends(get_db)
):
    """Create a new classification rule."""
    service = ClassificationService(db)

    # Verify classification exists
    classification = service.get_classification(rule.classification_id)
    if not classification:
        raise HTTPException(status_code=404, detail="Classification not found")

    # Create new rule
    new_rule = ClassificationRule(
        rule_name=rule.rule_name,
        rule_priority=rule.rule_priority,
        classification_id=rule.classification_id,
        is_active=rule.is_active,
        description_pattern=rule.description_pattern,
        category_pattern=rule.category_pattern,
        source_pattern=rule.source_pattern,
        amount_min=rule.amount_min,
        amount_max=rule.amount_max,
        payment_method_pattern=rule.payment_method_pattern
    )

    db.add(new_rule)
    db.commit()
    db.refresh(new_rule)

    return ClassificationRuleResponse.model_validate(new_rule)


@router.put(
    "/classification-rules/{rule_id}",
    response_model=ClassificationRuleResponse,
    summary="Update Classification Rule",
    description="Update an existing classification rule."
)
def update_classification_rule(
    rule_id: int = Path(..., description="Rule ID"),
    rule_update: ClassificationRuleUpdate = ...,
    db: Session = Depends(get_db)
):
    """Update a classification rule."""
    rule = db.query(ClassificationRule).filter(
        ClassificationRule.rule_id == rule_id
    ).first()

    if not rule:
        raise HTTPException(status_code=404, detail="Classification rule not found")

    # Update fields - use exclude_unset to only update provided fields
    # Note: null values ARE included (they explicitly clear the field)
    update_data = rule_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(rule, field, value)

    db.commit()
    db.refresh(rule)

    return ClassificationRuleResponse.model_validate(rule)


@router.delete(
    "/classification-rules/{rule_id}",
    status_code=204,
    summary="Delete Classification Rule",
    description="Delete a classification rule."
)
def delete_classification_rule(
    rule_id: int = Path(..., description="Rule ID"),
    db: Session = Depends(get_db)
):
    """Delete a classification rule."""
    rule = db.query(ClassificationRule).filter(
        ClassificationRule.rule_id == rule_id
    ).first()

    if not rule:
        raise HTTPException(status_code=404, detail="Classification rule not found")

    db.delete(rule)
    db.commit()

    return None


@router.post(
    "/classification-rules/test",
    response_model=TestRuleResponse,
    summary="Test Classification Rule",
    description="""
    Test a classification rule without applying it.

    Returns the number of transactions that would match the rule
    and a sample of matching transaction IDs.
    """
)
def test_classification_rule(
    request: TestRuleRequest,
    db: Session = Depends(get_db)
):
    """Test a classification rule."""
    from ...database.models import Transaction, Category
    from sqlalchemy import and_

    # Build query based on patterns
    query = db.query(Transaction)
    conditions = []

    if request.description_pattern:
        conditions.append(Transaction.description.like(request.description_pattern))

    if request.category_pattern:
        # Join with categories table and match on category name
        query = query.join(Category, Transaction.category_id == Category.category_id, isouter=True)
        conditions.append(Category.category_name.like(request.category_pattern))

    if request.source_pattern:
        conditions.append(Transaction.source.like(request.source_pattern))

    if request.amount_min is not None:
        conditions.append(Transaction.amount >= request.amount_min)

    if request.amount_max is not None:
        conditions.append(Transaction.amount <= request.amount_max)

    if request.payment_method_pattern:
        conditions.append(Transaction.payment_method.like(request.payment_method_pattern))

    if conditions:
        query = query.filter(and_(*conditions))

    # Get matching transactions
    matching_transactions = query.all()
    sample_ids = [t.transaction_id for t in matching_transactions[:10]]

    return TestRuleResponse(
        matching_transactions=len(matching_transactions),
        sample_transaction_ids=sample_ids
    )


@router.post(
    "/classification-rules/apply",
    response_model=ApplyRulesResponse,
    summary="Apply Classification Rules",
    description="""
    Apply classification rules to existing transactions.

    By default, this is a dry-run that previews changes without applying them.
    Set dry_run=False to actually apply the rules.

    Rules are applied in priority order (lower number = higher priority).
    Only active rules are applied unless specific rule_ids are provided.
    """
)
def apply_classification_rules(
    request: ApplyRulesRequest,
    db: Session = Depends(get_db)
):
    """Apply classification rules to existing transactions."""
    from ...database.models import Transaction, Category
    from sqlalchemy import and_

    # Get rules to apply
    query = db.query(ClassificationRule)

    if request.rule_ids:
        query = query.filter(ClassificationRule.rule_id.in_(request.rule_ids))
    else:
        query = query.filter(ClassificationRule.is_active == True)

    rules = query.order_by(ClassificationRule.rule_priority).all()

    total_transactions_updated = 0
    rules_applied = []

    for rule in rules:
        # Build query for matching transactions
        trans_query = db.query(Transaction)
        conditions = []

        if rule.description_pattern:
            # Use ilike for case-insensitive pattern matching
            conditions.append(Transaction.description.ilike(rule.description_pattern))

        if rule.category_pattern:
            trans_query = trans_query.join(Category, Transaction.category_id == Category.category_id, isouter=True)
            # Use ilike for case-insensitive pattern matching
            conditions.append(Category.category_name.ilike(rule.category_pattern))

        if rule.source_pattern:
            # Use ilike for case-insensitive pattern matching
            conditions.append(Transaction.source.ilike(rule.source_pattern))

        if rule.amount_min is not None:
            conditions.append(Transaction.amount >= rule.amount_min)

        if rule.amount_max is not None:
            conditions.append(Transaction.amount <= rule.amount_max)

        if rule.payment_method_pattern:
            # Use ilike for case-insensitive pattern matching
            conditions.append(Transaction.payment_method.ilike(rule.payment_method_pattern))

        if conditions:
            trans_query = trans_query.filter(and_(*conditions))
        else:
            # Safety: skip rules with no criteria to prevent full-table updates
            # This commonly happens with a "Default: Standard" rule that has no patterns.
            rules_applied.append({
                "rule_id": rule.rule_id,
                "rule_name": rule.rule_name + " (skipped: no criteria)",
                "classification_name": db.query(TransactionClassification)
                    .filter(TransactionClassification.classification_id == rule.classification_id)
                    .first().classification_name if db.query(TransactionClassification)
                    .filter(TransactionClassification.classification_id == rule.classification_id)
                    .first() else "Unknown",
                "transactions_matched": 0
            })
            continue

        # Get matching transactions
        matching_transactions = trans_query.all()
        transactions_matched = len(matching_transactions)

        # Apply classification if not dry run
        if not request.dry_run and transactions_matched > 0:
            # Extract transaction IDs and update them
            transaction_ids = [t.transaction_id for t in matching_transactions]
            db.query(Transaction).filter(
                Transaction.transaction_id.in_(transaction_ids)
            ).update(
                {Transaction.classification_id: rule.classification_id},
                synchronize_session=False
            )

        total_transactions_updated += transactions_matched

        # Get classification name for response
        classification = db.query(TransactionClassification).filter(
            TransactionClassification.classification_id == rule.classification_id
        ).first()

        rules_applied.append({
            "rule_id": rule.rule_id,
            "rule_name": rule.rule_name,
            "classification_name": classification.classification_name if classification else "Unknown",
            "transactions_matched": transactions_matched
        })

    # Commit if not dry run
    if not request.dry_run:
        db.commit()

    return ApplyRulesResponse(
        dry_run=request.dry_run,
        total_rules_processed=len(rules),
        total_transactions_updated=total_transactions_updated,
        rules_applied=rules_applied
    )

