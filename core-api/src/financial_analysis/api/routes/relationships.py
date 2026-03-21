"""Relationship detection and management API endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..schemas.relationship import (
    RelationshipResponse,
    RelationshipCreateRequest,
    TransferPairsResponse,
    CreditCardPairsResponse,
    ReimbursementPairsResponse,
    DividendReinvestmentPairsResponse,
    DetectAllRelationshipsResponse,
    RelatedTransactionsResponse,
    TransactionSummary,
    TransferPairDetection,
    CreditCardPairDetection,
    ReimbursementPairDetection,
    DividendReinvestmentPairDetection,
    RelatedTransactionInfo
)
from ..schemas.common import SuccessResponse
from ...services.relationship_service import RelationshipService

router = APIRouter()


@router.post("/relationships/detect/transfers", response_model=TransferPairsResponse)
def detect_transfer_pairs(
    date_tolerance_days: int = Query(3, ge=1, le=30, description="Maximum days between transactions"),
    amount_tolerance: float = Query(0.01, ge=0, description="Maximum amount difference"),
    auto_link: bool = Query(False, description="Automatically create relationships for high-confidence matches"),
    db: Session = Depends(get_db)
):
    """
    Detect potential transfer pairs (same amount, within date range).
    
    Transfer pairs are transactions that represent money moving between accounts,
    such as transfers from checking to savings or between different banks.
    
    Args:
        date_tolerance_days: Maximum days between transactions (default: 3)
        amount_tolerance: Maximum amount difference to consider a match (default: 0.01)
        auto_link: If True, automatically create relationships for high-confidence matches (>=0.8)
        db: Database session
        
    Returns:
        TransferPairsResponse: Detected transfer pairs with confidence scores
    """
    service = RelationshipService(db)
    
    try:
        from decimal import Decimal
        result = service.detect_transfer_pairs(
            date_tolerance_days=date_tolerance_days,
            amount_tolerance=Decimal(str(amount_tolerance)),
            auto_link=auto_link
        )
        
        # Convert to response format
        pairs = []
        for pair in result:
            tx1 = pair['transaction_1']
            tx2 = pair['transaction_2']
            
            pairs.append(TransferPairDetection(
                transaction_1=TransactionSummary(
                    transaction_id=tx1.transaction_id,
                    transaction_date=tx1.transaction_date,
                    amount=tx1.amount,
                    transaction_type=tx1.transaction_type,
                    description=tx1.description,
                    source=tx1.source,
                    category_name=tx1.category.category_name if tx1.category else None,
                ),
                transaction_2=TransactionSummary(
                    transaction_id=tx2.transaction_id,
                    transaction_date=tx2.transaction_date,
                    amount=tx2.amount,
                    transaction_type=tx2.transaction_type,
                    description=tx2.description,
                    source=tx2.source,
                    category_name=tx2.category.category_name if tx2.category else None,
                ),
                confidence=pair['confidence'],
                amount_difference=pair['amount_difference'],
                date_difference_days=pair['date_difference_days'],
                relationship_type=pair['relationship_type']
            ))
        
        return TransferPairsResponse(
            count=len(pairs),
            high_confidence=len([p for p in pairs if p.confidence >= 0.8]),
            pairs=pairs
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to detect transfer pairs: {str(e)}")


@router.post("/relationships/detect/credit-cards", response_model=CreditCardPairsResponse)
def detect_credit_card_pairs(
    date_tolerance_days: int = Query(5, ge=1, le=30, description="Maximum days between payment and receipt"),
    auto_link: bool = Query(False, description="Automatically create relationships for high-confidence matches"),
    db: Session = Depends(get_db)
):
    """
    Detect credit card payment/receipt pairs.
    
    Identifies matching pairs of credit card payments (from bank account) and
    receipts (to credit card company) to prevent double-counting in analysis.
    
    Args:
        date_tolerance_days: Maximum days between payment and receipt (default: 5)
        auto_link: If True, automatically create relationships for high-confidence matches (>=0.8)
        db: Database session
        
    Returns:
        CreditCardPairsResponse: Detected credit card pairs with confidence scores
    """
    service = RelationshipService(db)
    
    try:
        result = service.detect_credit_card_payments(
            date_tolerance_days=date_tolerance_days,
            auto_link=auto_link
        )
        
        # Convert to response format
        pairs = []
        for pair in result:
            payment = pair['payment']
            receipt = pair['receipt']
            
            pairs.append(CreditCardPairDetection(
                payment=TransactionSummary(
                    transaction_id=payment.transaction_id,
                    transaction_date=payment.transaction_date,
                    amount=payment.amount,
                    transaction_type=payment.transaction_type,
                    description=payment.description,
                    source=payment.source,
                    category_name=payment.category.category_name if payment.category else None,
                ),
                receipt=TransactionSummary(
                    transaction_id=receipt.transaction_id,
                    transaction_date=receipt.transaction_date,
                    amount=receipt.amount,
                    transaction_type=receipt.transaction_type,
                    description=receipt.description,
                    source=receipt.source,
                    category_name=receipt.category.category_name if receipt.category else None,
                ),
                confidence=pair['confidence'],
                date_difference_days=pair['date_difference_days'],
                relationship_type=pair['relationship_type']
            ))
        
        return CreditCardPairsResponse(
            count=len(pairs),
            high_confidence=len([p for p in pairs if p.confidence >= 0.8]),
            pairs=pairs
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to detect credit card pairs: {str(e)}")


@router.post("/relationships/detect/reimbursements", response_model=ReimbursementPairsResponse)
def detect_reimbursement_pairs(
    date_tolerance_days: int = Query(30, ge=1, le=90, description="Maximum days between expense and reimbursement"),
    auto_link: bool = Query(False, description="Automatically create relationships for high-confidence matches"),
    db: Session = Depends(get_db)
):
    """
    Detect reimbursement pairs (expense paid + reimbursement received).
    
    Identifies expenses that were later reimbursed to properly track
    out-of-pocket costs vs. reimbursed amounts.
    
    Args:
        date_tolerance_days: Maximum days between expense and reimbursement (default: 30)
        auto_link: If True, automatically create relationships for high-confidence matches (>=0.8)
        db: Database session
        
    Returns:
        ReimbursementPairsResponse: Detected reimbursement pairs with confidence scores
    """
    service = RelationshipService(db)
    
    try:
        result = service.detect_reimbursement_pairs(
            date_tolerance_days=date_tolerance_days,
            auto_link=auto_link
        )
        
        # Convert to response format
        pairs = []
        for pair in result:
            expense = pair['expense']
            reimbursement = pair['reimbursement']
            
            pairs.append(ReimbursementPairDetection(
                expense=TransactionSummary(
                    transaction_id=expense.transaction_id,
                    transaction_date=expense.transaction_date,
                    amount=expense.amount,
                    transaction_type=expense.transaction_type,
                    description=expense.description,
                    source=expense.source,
                    category_name=expense.category.category_name if expense.category else None,
                ),
                reimbursement=TransactionSummary(
                    transaction_id=reimbursement.transaction_id,
                    transaction_date=reimbursement.transaction_date,
                    amount=reimbursement.amount,
                    transaction_type=reimbursement.transaction_type,
                    description=reimbursement.description,
                    source=reimbursement.source,
                    category_name=reimbursement.category.category_name if reimbursement.category else None,
                ),
                confidence=pair['confidence'],
                date_difference_days=pair['date_difference_days'],
                relationship_type=pair['relationship_type']
            ))
        
        return ReimbursementPairsResponse(
            count=len(pairs),
            high_confidence=len([p for p in pairs if p.confidence >= 0.8]),
            pairs=pairs
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to detect reimbursement pairs: {str(e)}")


@router.post("/relationships/detect/dividend-reinvestments", response_model=DividendReinvestmentPairsResponse)
def detect_dividend_reinvestment_pairs(
    date_tolerance_days: int = Query(1, ge=1, le=7, description="Maximum days between dividend and reinvestment"),
    amount_tolerance: float = Query(0.01, ge=0, description="Maximum amount difference"),
    auto_link: bool = Query(False, description="Automatically create relationships for high-confidence matches"),
    db: Session = Depends(get_db)
):
    """
    Detect dividend reinvestment pairs (dividend income + automatic reinvestment).

    Identifies dividend income transactions that were automatically reinvested
    in the same security. Links the dividend (income) with the reinvestment (expense).

    Args:
        date_tolerance_days: Maximum days between dividend and reinvestment (default: 1)
        amount_tolerance: Maximum amount difference to consider a match (default: 0.01)
        auto_link: If True, automatically create relationships for high-confidence matches (>=0.8)
        db: Database session

    Returns:
        DividendReinvestmentPairsResponse: Detected dividend reinvestment pairs with confidence scores
    """
    service = RelationshipService(db)

    try:
        from decimal import Decimal
        result = service.detect_dividend_reinvestment_pairs(
            date_tolerance_days=date_tolerance_days,
            amount_tolerance=Decimal(str(amount_tolerance)),
            auto_link=auto_link
        )

        # Convert to response format
        pairs = []
        for pair in result:
            dividend = pair['dividend']
            reinvestment = pair['reinvestment']

            pairs.append(DividendReinvestmentPairDetection(
                dividend=TransactionSummary(
                    transaction_id=dividend.transaction_id,
                    transaction_date=dividend.transaction_date,
                    amount=dividend.amount,
                    transaction_type=dividend.transaction_type,
                    description=dividend.description,
                    source=dividend.source,
                    category_name=dividend.category.category_name if dividend.category else None,
                ),
                reinvestment=TransactionSummary(
                    transaction_id=reinvestment.transaction_id,
                    transaction_date=reinvestment.transaction_date,
                    amount=reinvestment.amount,
                    transaction_type=reinvestment.transaction_type,
                    description=reinvestment.description,
                    source=reinvestment.source,
                    category_name=reinvestment.category.category_name if reinvestment.category else None,
                ),
                confidence=pair['confidence'],
                amount_difference=pair['amount_difference'],
                date_difference_days=pair['date_difference_days'],
                relationship_type=pair['relationship_type']
            ))

        return DividendReinvestmentPairsResponse(
            count=len(pairs),
            high_confidence=len([p for p in pairs if p.confidence >= 0.8]),
            pairs=pairs
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to detect dividend reinvestment pairs: {str(e)}")


@router.post("/relationships/detect/all", response_model=DetectAllRelationshipsResponse)
def detect_all_relationships(
    auto_link: bool = Query(False, description="Automatically create relationships for high-confidence matches"),
    date_tolerance_days: int = Query(3, ge=1, le=30, description="Maximum days between related transactions"),
    db: Session = Depends(get_db)
):
    """
    Run all relationship detection algorithms.

    Detects transfer pairs, credit card payments, reimbursements, and dividend reinvestments in a single operation.

    Args:
        auto_link: If True, automatically create relationships for high-confidence matches (>=0.8)
        date_tolerance_days: Maximum days between related transactions (for transfers)
        db: Database session

    Returns:
        DetectAllRelationshipsResponse: Summary of all detected relationships
    """
    service = RelationshipService(db)

    try:
        result = service.detect_all_relationships(
            auto_link=auto_link,
            date_tolerance_days=date_tolerance_days
        )

        # Convert transfer pairs
        transfer_pairs = []
        for pair in result['transfer_pairs']['pairs']:
            tx1 = pair['transaction_1']
            tx2 = pair['transaction_2']
            transfer_pairs.append(TransferPairDetection(
                transaction_1=TransactionSummary(
                    transaction_id=tx1.transaction_id,
                    transaction_date=tx1.transaction_date,
                    amount=tx1.amount,
                    transaction_type=tx1.transaction_type,
                    description=tx1.description,
                    source=tx1.source,
                    category_name=tx1.category.category_name if tx1.category else None,
                ),
                transaction_2=TransactionSummary(
                    transaction_id=tx2.transaction_id,
                    transaction_date=tx2.transaction_date,
                    amount=tx2.amount,
                    transaction_type=tx2.transaction_type,
                    description=tx2.description,
                    source=tx2.source,
                    category_name=tx2.category.category_name if tx2.category else None,
                ),
                confidence=pair['confidence'],
                amount_difference=pair['amount_difference'],
                date_difference_days=pair['date_difference_days'],
                relationship_type=pair['relationship_type']
            ))

        # Convert credit card pairs
        cc_pairs = []
        for pair in result['credit_card_pairs']['pairs']:
            payment = pair['payment']
            receipt = pair['receipt']
            cc_pairs.append(CreditCardPairDetection(
                payment=TransactionSummary(
                    transaction_id=payment.transaction_id,
                    transaction_date=payment.transaction_date,
                    amount=payment.amount,
                    transaction_type=payment.transaction_type,
                    description=payment.description,
                    source=payment.source,
                    category_name=payment.category.category_name if payment.category else None,
                ),
                receipt=TransactionSummary(
                    transaction_id=receipt.transaction_id,
                    transaction_date=receipt.transaction_date,
                    amount=receipt.amount,
                    transaction_type=receipt.transaction_type,
                    description=receipt.description,
                    source=receipt.source,
                    category_name=receipt.category.category_name if receipt.category else None,
                ),
                confidence=pair['confidence'],
                date_difference_days=pair['date_difference_days'],
                relationship_type=pair['relationship_type']
            ))

        # Convert reimbursement pairs
        reimb_pairs = []
        for pair in result['reimbursement_pairs']['pairs']:
            expense = pair['expense']
            reimbursement = pair['reimbursement']
            reimb_pairs.append(ReimbursementPairDetection(
                expense=TransactionSummary(
                    transaction_id=expense.transaction_id,
                    transaction_date=expense.transaction_date,
                    amount=expense.amount,
                    transaction_type=expense.transaction_type,
                    description=expense.description,
                    source=expense.source,
                    category_name=expense.category.category_name if expense.category else None,
                ),
                reimbursement=TransactionSummary(
                    transaction_id=reimbursement.transaction_id,
                    transaction_date=reimbursement.transaction_date,
                    amount=reimbursement.amount,
                    transaction_type=reimbursement.transaction_type,
                    description=reimbursement.description,
                    source=reimbursement.source,
                    category_name=reimbursement.category.category_name if reimbursement.category else None,
                ),
                confidence=pair['confidence'],
                date_difference_days=pair['date_difference_days'],
                relationship_type=pair['relationship_type']
            ))

        # Convert dividend reinvestment pairs
        dividend_pairs = []
        for pair in result['dividend_reinvestment_pairs']['pairs']:
            dividend = pair['dividend']
            reinvestment = pair['reinvestment']
            dividend_pairs.append(DividendReinvestmentPairDetection(
                dividend=TransactionSummary(
                    transaction_id=dividend.transaction_id,
                    transaction_date=dividend.transaction_date,
                    amount=dividend.amount,
                    transaction_type=dividend.transaction_type,
                    description=dividend.description,
                    source=dividend.source,
                    category_name=dividend.category.category_name if dividend.category else None,
                ),
                reinvestment=TransactionSummary(
                    transaction_id=reinvestment.transaction_id,
                    transaction_date=reinvestment.transaction_date,
                    amount=reinvestment.amount,
                    transaction_type=reinvestment.transaction_type,
                    description=reinvestment.description,
                    source=reinvestment.source,
                    category_name=reinvestment.category.category_name if reinvestment.category else None,
                ),
                confidence=pair['confidence'],
                amount_difference=pair['amount_difference'],
                date_difference_days=pair['date_difference_days'],
                relationship_type=pair['relationship_type']
            ))

        return DetectAllRelationshipsResponse(
            transfer_pairs=TransferPairsResponse(
                count=result['transfer_pairs']['count'],
                high_confidence=result['transfer_pairs']['high_confidence'],
                pairs=transfer_pairs
            ),
            credit_card_pairs=CreditCardPairsResponse(
                count=result['credit_card_pairs']['count'],
                high_confidence=result['credit_card_pairs']['high_confidence'],
                pairs=cc_pairs
            ),
            reimbursement_pairs=ReimbursementPairsResponse(
                count=result['reimbursement_pairs']['count'],
                high_confidence=result['reimbursement_pairs']['high_confidence'],
                pairs=reimb_pairs
            ),
            dividend_reinvestment_pairs=DividendReinvestmentPairsResponse(
                count=result['dividend_reinvestment_pairs']['count'],
                high_confidence=result['dividend_reinvestment_pairs']['high_confidence'],
                pairs=dividend_pairs
            ),
            total_detected=result['total_detected'],
            auto_linked=result['auto_linked']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to detect relationships: {str(e)}")


@router.post("/relationships", response_model=RelationshipResponse)
def create_relationship(
    request: RelationshipCreateRequest,
    db: Session = Depends(get_db)
):
    """
    Manually create a relationship between two transactions.

    Args:
        request: Relationship creation request
        db: Database session

    Returns:
        RelationshipResponse: Created relationship
    """
    service = RelationshipService(db)

    try:
        relationship = service.create_relationship(
            transaction_id_1=request.transaction_id_1,
            transaction_id_2=request.transaction_id_2,
            relationship_type=request.relationship_type,
            description=request.description
        )

        if not relationship:
            raise HTTPException(
                status_code=404,
                detail="One or both transactions not found"
            )

        return RelationshipResponse(
            relationship_id=relationship.relationship_id,
            transaction_id_1=relationship.transaction_id_1,
            transaction_id_2=relationship.transaction_id_2,
            relationship_type=relationship.relationship_type,
            description=relationship.description,
            created_at=relationship.created_at.isoformat()
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create relationship: {str(e)}")


@router.get("/transactions/{transaction_id}/relationships", response_model=RelatedTransactionsResponse)
def get_related_transactions(
    transaction_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all transactions related to a given transaction.

    Args:
        transaction_id: Transaction ID
        db: Database session

    Returns:
        RelatedTransactionsResponse: Related transactions with relationship info
    """
    service = RelationshipService(db)

    try:
        related = service.get_related_transactions(transaction_id)

        related_info = []
        for rel in related:
            tx = rel['transaction']
            related_info.append(RelatedTransactionInfo(
                transaction=TransactionSummary(
                    transaction_id=tx.transaction_id,
                    transaction_date=tx.transaction_date,
                    amount=tx.amount,
                    transaction_type=tx.transaction_type,
                    description=tx.description,
                    source=tx.source,
                    category_name=tx.category.category_name if tx.category else None,
                ),
                relationship_type=rel['relationship_type'],
                relationship_description=rel['relationship_description']
            ))

        return RelatedTransactionsResponse(
            transaction_id=transaction_id,
            related_transactions=related_info,
            count=len(related_info)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get related transactions: {str(e)}")


@router.delete("/relationships/{relationship_id}", response_model=SuccessResponse)
def delete_relationship(
    relationship_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a relationship between transactions.

    Args:
        relationship_id: Relationship ID to delete
        db: Database session

    Returns:
        SuccessResponse: Success confirmation
    """
    service = RelationshipService(db)

    try:
        success = service.delete_relationship(relationship_id)

        if not success:
            raise HTTPException(
                status_code=404,
                detail=f"Relationship {relationship_id} not found"
            )

        return SuccessResponse(
            success=True,
            message=f"Relationship {relationship_id} deleted successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete relationship: {str(e)}")

