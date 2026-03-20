"""Transaction classification service."""

import logging
from typing import Optional, List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from datetime import datetime, timedelta
from decimal import Decimal
import re

logger = logging.getLogger(__name__)

from ..database.models import (
    Transaction, TransactionClassification, ClassificationRule,
    TransactionRelationship
)


class ClassificationService:
    """Service for transaction classification and relationship management."""
    
    def __init__(self, db: Session):
        """
        Initialize classification service.
        
        Args:
            db: Database session
        """
        self.db = db
    
    def get_classification(self, classification_id: int) -> Optional[TransactionClassification]:
        """
        Get classification by ID.
        
        Args:
            classification_id: Classification ID
            
        Returns:
            Optional[TransactionClassification]: Classification if found
        """
        return self.db.query(TransactionClassification).filter(
            TransactionClassification.classification_id == classification_id
        ).first()
    
    def get_classification_by_code(self, code: str) -> Optional[TransactionClassification]:
        """
        Get classification by code.
        
        Args:
            code: Classification code
            
        Returns:
            Optional[TransactionClassification]: Classification if found
        """
        return self.db.query(TransactionClassification).filter(
            TransactionClassification.classification_code == code
        ).first()
    
    def list_classifications(
        self,
        include_system_only: bool = False
    ) -> List[TransactionClassification]:
        """
        List all classifications.
        
        Args:
            include_system_only: If True, only return system classifications
            
        Returns:
            List[TransactionClassification]: List of classifications
        """
        query = self.db.query(TransactionClassification)
        
        if include_system_only:
            query = query.filter(TransactionClassification.is_system_classification == True)
        
        return query.order_by(TransactionClassification.classification_name).all()
    
    def classify_transaction(
        self,
        transaction_id: int,
        classification_id: int
    ) -> Optional[Transaction]:
        """
        Manually classify a transaction.
        
        Args:
            transaction_id: Transaction ID
            classification_id: Classification ID
            
        Returns:
            Optional[Transaction]: Updated transaction if found
        """
        transaction = self.db.query(Transaction).filter(
            Transaction.transaction_id == transaction_id
        ).first()

        if not transaction:
            return None
        
        classification = self.get_classification(classification_id)
        if not classification:
            return None
        
        transaction.classification_id = classification_id
        
        # Update flags based on classification
        if classification.classification_code == 'TRANSFER':
            transaction.is_transfer = True
            transaction.include_in_analysis = False
        elif classification.classification_code in ['CC_PAYMENT', 'CC_RECEIPT']:
            transaction.is_transfer = True
            transaction.include_in_analysis = False
        
        self.db.commit()
        self.db.refresh(transaction)
        
        return transaction
    
    def auto_classify_transaction(self, transaction: Transaction) -> bool:
        """
        Automatically classify a transaction based on rules.
        
        Args:
            transaction: Transaction to classify
            
        Returns:
            bool: True if classification was applied
        """
        # Get active rules ordered by priority
        rules = self.db.query(ClassificationRule).filter(
            ClassificationRule.is_active == True
        ).order_by(ClassificationRule.rule_priority).all()
        
        for rule in rules:
            if self._rule_matches(transaction, rule):
                # Apply classification
                transaction.classification_id = rule.classification_id

                # Apply actions
                if rule.set_include_in_analysis is not None:
                    transaction.include_in_analysis = rule.set_include_in_analysis

                if rule.set_is_transfer is not None:
                    transaction.is_transfer = rule.set_is_transfer

                return True

        # No rule matched — assign default classification (Standard/Regular Transaction)
        # Prefer STANDARD; fall back to REGULAR; finally, try by name contains 'Regular'/'Standard'
        default_cls = self.get_classification_by_code('STANDARD')
        if not default_cls:
            default_cls = self.get_classification_by_code('REGULAR')
        if not default_cls:
            default_cls = self.db.query(TransactionClassification).filter(
                (TransactionClassification.classification_name.ilike('%regular%')) |
                (TransactionClassification.classification_name.ilike('%standard%'))
            ).first()
        if default_cls:
            transaction.classification_id = default_cls.classification_id
            return True

        return False

    def auto_classify_all_unclassified(self) -> Dict[str, int]:
        """
        Automatically classify all unclassified transactions.
        
        Returns:
            Dict[str, int]: Statistics about classification
        """
        unclassified = self.db.query(Transaction).filter(
            Transaction.classification_id == None
        ).all()
        
        classified_count = 0
        
        for transaction in unclassified:
            if self.auto_classify_transaction(transaction):
                classified_count += 1
        
        self.db.commit()
        
        return {
            'total_unclassified': len(unclassified),
            'classified': classified_count,
            'remaining_unclassified': len(unclassified) - classified_count
        }
    
    def create_relationship(
        self,
        transaction_id_1: int,
        transaction_id_2: int,
        relationship_type: str,
        description: Optional[str] = None
    ) -> Optional[TransactionRelationship]:
        """
        Create a relationship between two transactions.
        
        Args:
            transaction_id_1: First transaction ID
            transaction_id_2: Second transaction ID
            relationship_type: Type of relationship
            description: Optional description
            
        Returns:
            Optional[TransactionRelationship]: Created relationship
        """
        # Verify both transactions exist
        tx1 = self.db.query(Transaction).filter(
            Transaction.transaction_id == transaction_id_1
        ).first()
        tx2 = self.db.query(Transaction).filter(
            Transaction.transaction_id == transaction_id_2
        ).first()
        
        if not tx1 or not tx2:
            return None
        
        # Check if relationship already exists
        existing = self.db.query(TransactionRelationship).filter(
            TransactionRelationship.transaction_id_1 == transaction_id_1,
            TransactionRelationship.transaction_id_2 == transaction_id_2,
            TransactionRelationship.relationship_type == relationship_type
        ).first()
        
        if existing:
            # Backfill convenience links if missing
            try:
                if not getattr(tx1, "related_transaction_id", None):
                    tx1.related_transaction_id = tx2.transaction_id
                if not getattr(tx2, "related_transaction_id", None):
                    tx2.related_transaction_id = tx1.transaction_id
                self.db.commit()
            except Exception as exc:
                logger.warning("Failed to backfill relationship links for transactions %s/%s: %s", tx1.transaction_id, tx2.transaction_id, exc)
            return existing

        # Create relationship
        relationship = TransactionRelationship(
            transaction_id_1=transaction_id_1,
            transaction_id_2=transaction_id_2,
            relationship_type=relationship_type,
            description=description
        )

        self.db.add(relationship)

        # Update convenience link on both transactions so the UI can show the chain
        try:
            tx1.related_transaction_id = tx2.transaction_id
            tx2.related_transaction_id = tx1.transaction_id
        except Exception as exc:
            logger.warning("Failed to set relationship links for transactions %s/%s: %s", tx1.transaction_id, tx2.transaction_id, exc)

        self.db.commit()
        self.db.refresh(relationship)

        return relationship

    def get_related_transactions(
        self,
        transaction_id: int
    ) -> List[Dict[str, Any]]:
        """
        Get all transactions related to a given transaction.
        
        Args:
            transaction_id: Transaction ID
            
        Returns:
            List[Dict[str, Any]]: List of related transactions with relationship info
        """
        relationships = self.db.query(TransactionRelationship).filter(
            (TransactionRelationship.transaction_id_1 == transaction_id) |
            (TransactionRelationship.transaction_id_2 == transaction_id)
        ).all()
        
        related = []
        for rel in relationships:
            # Determine which is the related transaction
            related_id = (
                rel.transaction_id_2 if rel.transaction_id_1 == transaction_id
                else rel.transaction_id_1
            )
            
            related_tx = self.db.query(Transaction).filter(
                Transaction.transaction_id == related_id
            ).first()
            
            if related_tx:
                related.append({
                    'transaction': related_tx,
                    'relationship_type': rel.relationship_type,
                    'relationship_description': rel.description
                })
        
        return related
    
    def _rule_matches(self, transaction: Transaction, rule: ClassificationRule) -> bool:
        """
        Check if a transaction matches a classification rule.
        
        Args:
            transaction: Transaction to check
            rule: Classification rule
            
        Returns:
            bool: True if transaction matches rule
        """
        # Check description pattern
        if rule.description_pattern:
            if not transaction.description:
                return False
            pattern = rule.description_pattern.replace('%', '.*')
            if not re.search(pattern, transaction.description, re.IGNORECASE):
                return False
        
        # Check category pattern
        if rule.category_pattern:
            category = self.db.query(Transaction).filter(
                Transaction.transaction_id == transaction.transaction_id
            ).first()
            if category and category.category:
                pattern = rule.category_pattern.replace('%', '.*')
                if not re.search(pattern, category.category.category_name, re.IGNORECASE):
                    return False
        
        # Check source pattern
        if rule.source_pattern:
            if not transaction.source:
                return False
            pattern = rule.source_pattern.replace('%', '.*')
            if not re.search(pattern, transaction.source, re.IGNORECASE):
                return False
        
        # Check amount range
        if rule.amount_min and transaction.amount < rule.amount_min:
            return False
        
        if rule.amount_max and transaction.amount > rule.amount_max:
            return False
        
        # Check payment method pattern
        if rule.payment_method_pattern:
            if not transaction.payment_method:
                return False
            pattern = rule.payment_method_pattern.replace('%', '.*')
            if not re.search(pattern, transaction.payment_method, re.IGNORECASE):
                return False
        
        # All conditions matched
        return True

    def detect_transfer_pairs(
        self,
        date_tolerance_days: int = 3,
        amount_tolerance: Decimal = Decimal('0.01'),
        auto_link: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Detect potential transfer pairs (same amount, opposite types, within date range).

        Args:
            date_tolerance_days: Maximum days between transactions (default: 3)
            amount_tolerance: Maximum amount difference to consider a match (default: 0.01)
            auto_link: If True, automatically create relationships for high-confidence matches

        Returns:
            List[Dict[str, Any]]: List of potential transfer pairs with confidence scores
        """
        # Get all unlinked transactions that could be transfers
        transactions = self.db.query(Transaction).filter(
            Transaction.classification_id.in_(
                self.db.query(TransactionClassification.classification_id).filter(
                    TransactionClassification.classification_code.in_(['TRANSFER', 'CC_PAYMENT', 'CC_RECEIPT'])
                )
            )
        ).order_by(Transaction.transaction_date, Transaction.amount).all()

        # PERFORMANCE OPTIMIZATION: Fetch all existing relationships once
        # Build a set of linked transaction ID pairs for O(1) lookup
        existing_relationships = self.db.query(TransactionRelationship).all()
        linked_pairs = set()
        for rel in existing_relationships:
            # Store both directions for easy lookup
            linked_pairs.add((rel.transaction_id_1, rel.transaction_id_2))
            linked_pairs.add((rel.transaction_id_2, rel.transaction_id_1))

        potential_pairs = []
        processed_ids = set()

        for i, tx1 in enumerate(transactions):
            if tx1.transaction_id in processed_ids:
                continue

            # Look for matching transactions
            for tx2 in transactions[i+1:]:
                if tx2.transaction_id in processed_ids:
                    continue

                # Check if already linked (O(1) lookup instead of database query)
                if (tx1.transaction_id, tx2.transaction_id) in linked_pairs:
                    continue

                # Calculate match score
                match_score = self._calculate_transfer_match_score(
                    tx1, tx2, date_tolerance_days, amount_tolerance
                )

                if match_score > 0:
                    pair_info = {
                        'transaction_1': tx1,
                        'transaction_2': tx2,
                        'confidence': match_score,
                        'amount_difference': abs(tx1.amount - tx2.amount),
                        'date_difference_days': abs((tx1.transaction_date - tx2.transaction_date).days),
                        'relationship_type': self._determine_relationship_type(tx1, tx2)
                    }

                    potential_pairs.append(pair_info)

                    # Auto-link high confidence matches
                    if auto_link and match_score >= 0.8:
                        self.create_relationship(
                            tx1.transaction_id,
                            tx2.transaction_id,
                            pair_info['relationship_type'],
                            f"Auto-detected with {match_score:.0%} confidence"
                        )
                        processed_ids.add(tx1.transaction_id)
                        processed_ids.add(tx2.transaction_id)

        # Sort by confidence (highest first)
        potential_pairs.sort(key=lambda x: x['confidence'], reverse=True)

        return potential_pairs

    def detect_credit_card_payments(
        self,
        date_tolerance_days: int = 5,
        auto_link: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Detect credit card payment/receipt pairs.

        Args:
            date_tolerance_days: Maximum days between payment and receipt (default: 5)
            auto_link: If True, automatically create relationships for high-confidence matches

        Returns:
            List[Dict[str, Any]]: List of potential credit card payment pairs
        """
        # Get credit card payments (expenses from bank account)
        cc_payment_classification = self.get_classification_by_code('CC_PAYMENT')
        cc_receipt_classification = self.get_classification_by_code('CC_RECEIPT')

        if not cc_payment_classification or not cc_receipt_classification:
            return []

        payments = self.db.query(Transaction).filter(
            Transaction.classification_id == cc_payment_classification.classification_id
        ).all()

        receipts = self.db.query(Transaction).filter(
            Transaction.classification_id == cc_receipt_classification.classification_id
        ).all()

        # PERFORMANCE OPTIMIZATION: Fetch all CC_PAYMENT_RECEIPT relationships once
        # Build a set of payment IDs that are already linked
        existing_relationships = self.db.query(TransactionRelationship).filter(
            TransactionRelationship.relationship_type == 'CC_PAYMENT_RECEIPT'
        ).all()
        linked_payment_ids = set()
        for rel in existing_relationships:
            linked_payment_ids.add(rel.transaction_id_1)
            linked_payment_ids.add(rel.transaction_id_2)

        potential_pairs = []

        for payment in payments:
            # Check if already linked (O(1) lookup instead of database query)
            if payment.transaction_id in linked_payment_ids:
                continue

            for receipt in receipts:
                # Check date proximity
                date_diff = abs((payment.transaction_date - receipt.transaction_date).days)
                if date_diff > date_tolerance_days:
                    continue

                # Check amount match (should be same or very close)
                amount_diff = abs(payment.amount - receipt.amount)
                if amount_diff > Decimal('0.01'):
                    continue

                # Calculate confidence
                confidence = 1.0 - (date_diff / date_tolerance_days) * 0.3

                pair_info = {
                    'payment': payment,
                    'receipt': receipt,
                    'confidence': confidence,
                    'date_difference_days': date_diff,
                    'relationship_type': 'CC_PAYMENT_RECEIPT'
                }

                potential_pairs.append(pair_info)

                # Auto-link high confidence matches
                if auto_link and confidence >= 0.8:
                    self.create_relationship(
                        payment.transaction_id,
                        receipt.transaction_id,
                        'CC_PAYMENT_RECEIPT',
                        f"Auto-detected credit card payment pair with {confidence:.0%} confidence"
                    )

        potential_pairs.sort(key=lambda x: x['confidence'], reverse=True)
        return potential_pairs

    def detect_reimbursement_pairs(
        self,
        date_tolerance_days: int = 30,
        auto_link: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Detect reimbursement pairs (expense paid + reimbursement received).

        Args:
            date_tolerance_days: Maximum days between expense and reimbursement (default: 30)
            auto_link: If True, automatically create relationships for high-confidence matches

        Returns:
            List[Dict[str, Any]]: List of potential reimbursement pairs
        """
        # Get reimbursement classifications
        reimb_paid = self.get_classification_by_code('REIMB_PAID')
        reimb_received = self.get_classification_by_code('REIMB_RECEIVED')

        if not reimb_paid or not reimb_received:
            return []

        expenses = self.db.query(Transaction).filter(
            Transaction.classification_id == reimb_paid.classification_id
        ).all()

        reimbursements = self.db.query(Transaction).filter(
            Transaction.classification_id == reimb_received.classification_id
        ).all()

        # PERFORMANCE OPTIMIZATION: Fetch all REIMBURSEMENT_PAIR relationships once
        # Build a set of expense IDs that are already linked
        existing_relationships = self.db.query(TransactionRelationship).filter(
            TransactionRelationship.relationship_type == 'REIMBURSEMENT_PAIR'
        ).all()
        linked_expense_ids = set()
        for rel in existing_relationships:
            linked_expense_ids.add(rel.transaction_id_1)
            linked_expense_ids.add(rel.transaction_id_2)

        potential_pairs = []

        for expense in expenses:
            # Check if already linked (O(1) lookup instead of database query)
            if expense.transaction_id in linked_expense_ids:
                continue

            for reimbursement in reimbursements:
                # Reimbursement should come after expense
                if reimbursement.transaction_date < expense.transaction_date:
                    continue

                # Check date proximity
                date_diff = (reimbursement.transaction_date - expense.transaction_date).days
                if date_diff > date_tolerance_days:
                    continue

                # Check amount match
                amount_diff = abs(expense.amount - reimbursement.amount)
                if amount_diff > Decimal('0.01'):
                    continue

                # Calculate confidence
                confidence = 1.0 - (date_diff / date_tolerance_days) * 0.4

                # Boost confidence if descriptions are similar
                if expense.description and reimbursement.description:
                    desc_similarity = self._calculate_description_similarity(
                        expense.description, reimbursement.description
                    )
                    confidence = min(1.0, confidence + desc_similarity * 0.2)

                pair_info = {
                    'expense': expense,
                    'reimbursement': reimbursement,
                    'confidence': confidence,
                    'date_difference_days': date_diff,
                    'relationship_type': 'REIMBURSEMENT_PAIR'
                }

                potential_pairs.append(pair_info)

                # Auto-link high confidence matches
                if auto_link and confidence >= 0.8:
                    self.create_relationship(
                        expense.transaction_id,
                        reimbursement.transaction_id,
                        'REIMBURSEMENT_PAIR',
                        f"Auto-detected reimbursement pair with {confidence:.0%} confidence"
                    )

        potential_pairs.sort(key=lambda x: x['confidence'], reverse=True)
        return potential_pairs

    def detect_dividend_reinvestment_pairs(
        self,
        date_tolerance_days: int = 1,
        amount_tolerance: Decimal = Decimal('0.01'),
        auto_link: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Detect dividend reinvestment pairs (dividend income + automatic reinvestment).

        Args:
            date_tolerance_days: Maximum days between dividend and reinvestment (default: 1)
            amount_tolerance: Maximum amount difference to consider a match (default: 0.01)
            auto_link: If True, automatically create relationships for high-confidence matches

        Returns:
            List[Dict[str, Any]]: List of potential dividend reinvestment pairs with confidence scores
        """
        # Get dividend income transactions (INVESTMENT_DISTRIBUTION classification)
        dividend_classification = self.get_classification_by_code('INVESTMENT_DISTRIBUTION')
        reinvestment_classification = self.get_classification_by_code('DIVIDEND_REINVESTMENT')

        if not dividend_classification:
            return []

        # Get all dividend income transactions
        dividends = self.db.query(Transaction).filter(
            Transaction.classification_id == dividend_classification.classification_id,
            Transaction.transaction_type == 'Income'
        ).order_by(Transaction.transaction_date, Transaction.amount).all()

        # Get all potential reinvestment expense transactions
        # Include both classified reinvestments and unclassified expenses that might be reinvestments
        reinvestment_query = self.db.query(Transaction).filter(
            Transaction.transaction_type == 'Expense'
        )

        if reinvestment_classification:
            # Include transactions with DIVIDEND_REINVESTMENT classification OR
            # transactions with descriptions containing reinvestment keywords
            reinvestment_query = reinvestment_query.filter(
                or_(
                    Transaction.classification_id == reinvestment_classification.classification_id,
                    Transaction.description.ilike('%reinvest%'),
                    Transaction.description.ilike('%drip%'),
                    Transaction.description.ilike('%auto reinvest%')
                )
            )
        else:
            # If no reinvestment classification exists, just look for description patterns
            reinvestment_query = reinvestment_query.filter(
                or_(
                    Transaction.description.ilike('%reinvest%'),
                    Transaction.description.ilike('%drip%'),
                    Transaction.description.ilike('%auto reinvest%')
                )
            )

        reinvestments = reinvestment_query.order_by(
            Transaction.transaction_date, Transaction.amount
        ).all()

        # PERFORMANCE OPTIMIZATION: Fetch all existing relationships once
        # Build a set of linked transaction ID pairs for O(1) lookup
        existing_relationships = self.db.query(TransactionRelationship).all()
        linked_pairs = set()
        for rel in existing_relationships:
            # Store both directions for easy lookup
            linked_pairs.add((rel.transaction_id_1, rel.transaction_id_2))
            linked_pairs.add((rel.transaction_id_2, rel.transaction_id_1))

        potential_pairs = []
        processed_ids = set()

        for dividend in dividends:
            if dividend.transaction_id in processed_ids:
                continue

            # Look for matching reinvestment transactions
            for reinvestment in reinvestments:
                if reinvestment.transaction_id in processed_ids:
                    continue

                # Check if already linked (O(1) lookup instead of database query)
                if (dividend.transaction_id, reinvestment.transaction_id) in linked_pairs:
                    continue

                # Calculate match score
                match_score = self._calculate_dividend_reinvestment_match_score(
                    dividend, reinvestment, date_tolerance_days, amount_tolerance
                )

                if match_score > 0:
                    pair_info = {
                        'dividend': dividend,
                        'reinvestment': reinvestment,
                        'confidence': match_score,
                        'amount_difference': abs(dividend.amount - reinvestment.amount),
                        'date_difference_days': abs((dividend.transaction_date - reinvestment.transaction_date).days),
                        'relationship_type': 'DIVIDEND_REINVESTMENT_PAIR'
                    }

                    potential_pairs.append(pair_info)

                    # Auto-link high confidence matches
                    if auto_link and match_score >= 0.8:
                        self.create_relationship(
                            dividend.transaction_id,
                            reinvestment.transaction_id,
                            'DIVIDEND_REINVESTMENT_PAIR',
                            f"Auto-detected dividend reinvestment pair with {match_score:.0%} confidence"
                        )
                        processed_ids.add(dividend.transaction_id)
                        processed_ids.add(reinvestment.transaction_id)

        potential_pairs.sort(key=lambda x: x['confidence'], reverse=True)
        return potential_pairs

    def detect_all_relationships(
        self,
        auto_link: bool = False,
        date_tolerance_days: int = 3
    ) -> Dict[str, Any]:
        """
        Run all relationship detection algorithms.

        Args:
            auto_link: If True, automatically create relationships for high-confidence matches
            date_tolerance_days: Maximum days between related transactions

        Returns:
            Dict[str, Any]: Summary of all detected relationships
        """
        transfer_pairs = self.detect_transfer_pairs(
            date_tolerance_days=date_tolerance_days,
            auto_link=auto_link
        )

        cc_pairs = self.detect_credit_card_payments(
            date_tolerance_days=5,
            auto_link=auto_link
        )

        reimb_pairs = self.detect_reimbursement_pairs(
            date_tolerance_days=30,
            auto_link=auto_link
        )

        dividend_pairs = self.detect_dividend_reinvestment_pairs(
            date_tolerance_days=1,
            auto_link=auto_link
        )

        return {
            'transfer_pairs': {
                'count': len(transfer_pairs),
                'high_confidence': len([p for p in transfer_pairs if p['confidence'] >= 0.8]),
                'pairs': transfer_pairs
            },
            'credit_card_pairs': {
                'count': len(cc_pairs),
                'high_confidence': len([p for p in cc_pairs if p['confidence'] >= 0.8]),
                'pairs': cc_pairs
            },
            'reimbursement_pairs': {
                'count': len(reimb_pairs),
                'high_confidence': len([p for p in reimb_pairs if p['confidence'] >= 0.8]),
                'pairs': reimb_pairs
            },
            'dividend_reinvestment_pairs': {
                'count': len(dividend_pairs),
                'high_confidence': len([p for p in dividend_pairs if p['confidence'] >= 0.8]),
                'pairs': dividend_pairs
            },
            'total_detected': len(transfer_pairs) + len(cc_pairs) + len(reimb_pairs) + len(dividend_pairs),
            'auto_linked': auto_link
        }

    def delete_relationship(
        self,
        relationship_id: int
    ) -> bool:
        """
        Delete a relationship between transactions.

        Args:
            relationship_id: Relationship ID to delete

        Returns:
            bool: True if deleted successfully
        """
        relationship = self.db.query(TransactionRelationship).filter(
            TransactionRelationship.relationship_id == relationship_id
        ).first()

        if not relationship:
            return False

        self.db.delete(relationship)
        self.db.commit()

        return True

    def _calculate_transfer_match_score(
        self,
        tx1: Transaction,
        tx2: Transaction,
        date_tolerance_days: int,
        amount_tolerance: Decimal
    ) -> float:
        """
        Calculate match score for potential transfer pair.

        Args:
            tx1: First transaction
            tx2: Second transaction
            date_tolerance_days: Maximum days between transactions
            amount_tolerance: Maximum amount difference

        Returns:
            float: Match score (0.0 to 1.0), 0 if no match
        """
        # Check amount match
        amount_diff = abs(tx1.amount - tx2.amount)
        if amount_diff > amount_tolerance:
            return 0.0

        # Check date proximity
        date_diff = abs((tx1.transaction_date - tx2.transaction_date).days)
        if date_diff > date_tolerance_days:
            return 0.0

        # Base score starts at 0.6
        score = 0.6

        # Perfect amount match adds 0.2
        if amount_diff == 0:
            score += 0.2
        else:
            score += 0.2 * (1 - float(amount_diff / amount_tolerance))

        # Same day adds 0.2, decreases with days apart
        if date_diff == 0:
            score += 0.2
        else:
            score += 0.2 * (1 - date_diff / date_tolerance_days)

        # Check for account information in description/source
        if self._has_account_indicators(tx1, tx2):
            score = min(1.0, score + 0.1)

        # Check for transfer keywords
        if self._has_transfer_keywords(tx1) or self._has_transfer_keywords(tx2):
            score = min(1.0, score + 0.1)

        return min(1.0, score)

    def _determine_relationship_type(
        self,
        tx1: Transaction,
        tx2: Transaction
    ) -> str:
        """
        Determine the type of relationship between two transactions.

        Args:
            tx1: First transaction
            tx2: Second transaction

        Returns:
            str: Relationship type
        """
        # Check classifications
        if tx1.classification and tx2.classification:
            codes = {tx1.classification.classification_code, tx2.classification.classification_code}

            if 'CC_PAYMENT' in codes and 'CC_RECEIPT' in codes:
                return 'CC_PAYMENT_RECEIPT'
            elif 'REIMB_PAID' in codes and 'REIMB_RECEIVED' in codes:
                return 'REIMBURSEMENT_PAIR'

        # Default to transfer pair
        return 'TRANSFER_PAIR'

    def _has_account_indicators(
        self,
        tx1: Transaction,
        tx2: Transaction
    ) -> bool:
        """
        Check if transactions have account indicators suggesting they're related.

        Args:
            tx1: First transaction
            tx2: Second transaction

        Returns:
            bool: True if account indicators found
        """
        # Check transfer account fields
        if tx1.transfer_account_from and tx2.transfer_account_to:
            if tx1.transfer_account_from == tx2.transfer_account_to:
                return True

        if tx1.transfer_account_to and tx2.transfer_account_from:
            if tx1.transfer_account_to == tx2.transfer_account_from:
                return True

        # Check source fields for account names
        if tx1.source and tx2.source:
            # Simple check for common words (could be enhanced)
            words1 = set(tx1.source.lower().split())
            words2 = set(tx2.source.lower().split())
            common_words = words1.intersection(words2)

            # If they share account-like words
            account_keywords = {'checking', 'savings', 'credit', 'card', 'account'}
            if common_words.intersection(account_keywords):
                return True

        return False

    def _has_transfer_keywords(
        self,
        tx: Transaction
    ) -> bool:
        """
        Check if transaction description contains transfer keywords.

        Args:
            tx: Transaction to check

        Returns:
            bool: True if transfer keywords found
        """
        if not tx.description:
            return False

        transfer_keywords = [
            'transfer', 'xfer', 'move', 'moved',
            'from account', 'to account',
            'internal', 'between accounts'
        ]

        desc_lower = tx.description.lower()
        return any(keyword in desc_lower for keyword in transfer_keywords)

    def _calculate_description_similarity(
        self,
        desc1: str,
        desc2: str
    ) -> float:
        """
        Calculate similarity between two descriptions.

        Args:
            desc1: First description
            desc2: Second description

        Returns:
            float: Similarity score (0.0 to 1.0)
        """
        if not desc1 or not desc2:
            return 0.0

        # Simple word-based similarity
        words1 = set(desc1.lower().split())
        words2 = set(desc2.lower().split())

        if not words1 or not words2:
            return 0.0

        # Jaccard similarity
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))

        return intersection / union if union > 0 else 0.0

    def _calculate_dividend_reinvestment_match_score(
        self,
        dividend: Transaction,
        reinvestment: Transaction,
        date_tolerance_days: int,
        amount_tolerance: Decimal
    ) -> float:
        """
        Calculate match score for potential dividend reinvestment pair.

        Args:
            dividend: Dividend income transaction
            reinvestment: Reinvestment expense transaction
            date_tolerance_days: Maximum days between transactions
            amount_tolerance: Maximum amount difference

        Returns:
            float: Match score (0.0 to 1.0), 0 if no match
        """
        # Check amount match
        amount_diff = abs(dividend.amount - reinvestment.amount)
        if amount_diff > amount_tolerance:
            return 0.0

        # Check date proximity
        date_diff = abs((dividend.transaction_date - reinvestment.transaction_date).days)
        if date_diff > date_tolerance_days:
            return 0.0

        # Base score starts at 0.6
        score = 0.6

        # Perfect amount match adds 0.2
        if amount_diff == 0:
            score += 0.2
        else:
            score += 0.2 * (1 - float(amount_diff / amount_tolerance))

        # Same day adds 0.2, decreases with days apart
        if date_diff == 0:
            score += 0.2
        elif date_diff == 1:
            score += 0.1
        # else: 0 points for 2+ days apart

        # Check for description similarity (both mention same stock/fund)
        if dividend.description and reinvestment.description:
            desc_similarity = self._calculate_description_similarity(
                dividend.description, reinvestment.description
            )
            if desc_similarity >= 0.5:
                score = min(1.0, score + 0.1)

        # Check for same source/account
        if dividend.source and reinvestment.source and dividend.source == reinvestment.source:
            score = min(1.0, score + 0.1)

        return min(1.0, score)

