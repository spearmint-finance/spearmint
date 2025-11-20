"""Relationship API schemas."""

from typing import Optional, List
from datetime import date
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict

from .analysis import DecimalBaseModel


class TransactionSummary(DecimalBaseModel):
    """Summary of a transaction for relationship display."""

    transaction_id: int = Field(..., description="Transaction ID")
    transaction_date: date = Field(..., description="Transaction date")
    amount: Decimal = Field(..., description="Transaction amount")
    transaction_type: str = Field(..., description="Income or Expense")
    description: Optional[str] = Field(None, description="Transaction description")
    source: Optional[str] = Field(None, description="Transaction source")
    category_name: Optional[str] = Field(None, description="Category name")
    classification_name: Optional[str] = Field(None, description="Classification name")

    model_config = ConfigDict(from_attributes=True)


class RelationshipResponse(BaseModel):
    """Response model for a transaction relationship."""
    
    relationship_id: int = Field(..., description="Relationship ID")
    transaction_id_1: int = Field(..., description="First transaction ID")
    transaction_id_2: int = Field(..., description="Second transaction ID")
    relationship_type: str = Field(..., description="Type of relationship")
    description: Optional[str] = Field(None, description="Relationship description")
    created_at: str = Field(..., description="Creation timestamp")
    
    model_config = ConfigDict(from_attributes=True)


class RelationshipCreateRequest(BaseModel):
    """Request to create a relationship between transactions."""
    
    transaction_id_1: int = Field(..., gt=0, description="First transaction ID")
    transaction_id_2: int = Field(..., gt=0, description="Second transaction ID")
    relationship_type: str = Field(
        ...,
        description="Relationship type (TRANSFER_PAIR, CC_PAYMENT_RECEIPT, REIMBURSEMENT_PAIR, etc.)"
    )
    description: Optional[str] = Field(None, description="Optional description")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "transaction_id_1": 1,
                "transaction_id_2": 2,
                "relationship_type": "TRANSFER_PAIR",
                "description": "Transfer from checking to savings"
            }
        }
    )


class TransferPairDetection(DecimalBaseModel):
    """Detected transfer pair."""

    transaction_1: TransactionSummary = Field(..., description="First transaction")
    transaction_2: TransactionSummary = Field(..., description="Second transaction")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0-1)")
    amount_difference: Decimal = Field(..., description="Difference in amounts")
    date_difference_days: int = Field(..., description="Days between transactions")
    relationship_type: str = Field(..., description="Suggested relationship type")


class CreditCardPairDetection(BaseModel):
    """Detected credit card payment/receipt pair."""
    
    payment: TransactionSummary = Field(..., description="Payment transaction")
    receipt: TransactionSummary = Field(..., description="Receipt transaction")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0-1)")
    date_difference_days: int = Field(..., description="Days between transactions")
    relationship_type: str = Field(..., description="Relationship type")


class ReimbursementPairDetection(BaseModel):
    """Detected reimbursement pair."""

    expense: TransactionSummary = Field(..., description="Original expense")
    reimbursement: TransactionSummary = Field(..., description="Reimbursement income")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0-1)")
    date_difference_days: int = Field(..., description="Days between transactions")
    relationship_type: str = Field(..., description="Relationship type")


class DividendReinvestmentPairDetection(DecimalBaseModel):
    """Detected dividend reinvestment pair."""

    dividend: TransactionSummary = Field(..., description="Dividend income transaction")
    reinvestment: TransactionSummary = Field(..., description="Reinvestment expense transaction")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0-1)")
    amount_difference: Decimal = Field(..., description="Difference in amounts")
    date_difference_days: int = Field(..., description="Days between transactions")
    relationship_type: str = Field(..., description="Relationship type")


class DetectTransferPairsRequest(DecimalBaseModel):
    """Request to detect transfer pairs."""

    date_tolerance_days: int = Field(
        3,
        ge=1,
        le=30,
        description="Maximum days between transactions"
    )
    amount_tolerance: Decimal = Field(
        Decimal('0.01'),
        ge=0,
        description="Maximum amount difference"
    )
    auto_link: bool = Field(
        False,
        description="Automatically create relationships for high-confidence matches"
    )


class DetectCreditCardPairsRequest(BaseModel):
    """Request to detect credit card payment pairs."""
    
    date_tolerance_days: int = Field(
        5,
        ge=1,
        le=30,
        description="Maximum days between payment and receipt"
    )
    auto_link: bool = Field(
        False,
        description="Automatically create relationships for high-confidence matches"
    )


class DetectReimbursementPairsRequest(BaseModel):
    """Request to detect reimbursement pairs."""

    date_tolerance_days: int = Field(
        30,
        ge=1,
        le=90,
        description="Maximum days between expense and reimbursement"
    )
    auto_link: bool = Field(
        False,
        description="Automatically create relationships for high-confidence matches"
    )


class DetectDividendReinvestmentPairsRequest(DecimalBaseModel):
    """Request to detect dividend reinvestment pairs."""

    date_tolerance_days: int = Field(
        1,
        ge=1,
        le=7,
        description="Maximum days between dividend and reinvestment"
    )
    amount_tolerance: Decimal = Field(
        Decimal('0.01'),
        ge=0,
        description="Maximum amount difference"
    )
    auto_link: bool = Field(
        False,
        description="Automatically create relationships for high-confidence matches"
    )


class DetectAllRelationshipsRequest(BaseModel):
    """Request to detect all relationship types."""
    
    auto_link: bool = Field(
        False,
        description="Automatically create relationships for high-confidence matches"
    )
    date_tolerance_days: int = Field(
        3,
        ge=1,
        le=30,
        description="Maximum days between related transactions (for transfers)"
    )


class TransferPairsResponse(BaseModel):
    """Response with detected transfer pairs."""
    
    count: int = Field(..., description="Total number of pairs detected")
    high_confidence: int = Field(..., description="Number of high-confidence pairs (>=0.8)")
    pairs: List[TransferPairDetection] = Field(..., description="List of detected pairs")


class CreditCardPairsResponse(BaseModel):
    """Response with detected credit card pairs."""
    
    count: int = Field(..., description="Total number of pairs detected")
    high_confidence: int = Field(..., description="Number of high-confidence pairs (>=0.8)")
    pairs: List[CreditCardPairDetection] = Field(..., description="List of detected pairs")


class ReimbursementPairsResponse(BaseModel):
    """Response with detected reimbursement pairs."""

    count: int = Field(..., description="Total number of pairs detected")
    high_confidence: int = Field(..., description="Number of high-confidence pairs (>=0.8)")
    pairs: List[ReimbursementPairDetection] = Field(..., description="List of detected pairs")


class DividendReinvestmentPairsResponse(BaseModel):
    """Response with detected dividend reinvestment pairs."""

    count: int = Field(..., description="Total number of pairs detected")
    high_confidence: int = Field(..., description="Number of high-confidence pairs (>=0.8)")
    pairs: List[DividendReinvestmentPairDetection] = Field(..., description="List of detected pairs")


class DetectAllRelationshipsResponse(BaseModel):
    """Response with all detected relationships."""

    transfer_pairs: TransferPairsResponse = Field(..., description="Transfer pair detections")
    credit_card_pairs: CreditCardPairsResponse = Field(..., description="Credit card pair detections")
    reimbursement_pairs: ReimbursementPairsResponse = Field(..., description="Reimbursement pair detections")
    dividend_reinvestment_pairs: DividendReinvestmentPairsResponse = Field(..., description="Dividend reinvestment pair detections")
    total_detected: int = Field(..., description="Total relationships detected across all types")
    auto_linked: bool = Field(..., description="Whether relationships were automatically created")


class RelatedTransactionInfo(BaseModel):
    """Information about a related transaction."""
    
    transaction: TransactionSummary = Field(..., description="Related transaction")
    relationship_type: str = Field(..., description="Type of relationship")
    relationship_description: Optional[str] = Field(None, description="Relationship description")


class RelatedTransactionsResponse(BaseModel):
    """Response with related transactions."""
    
    transaction_id: int = Field(..., description="Original transaction ID")
    related_transactions: List[RelatedTransactionInfo] = Field(..., description="List of related transactions")
    count: int = Field(..., description="Number of related transactions")

