"""Transaction relationship detection and management service.

Extracted from ClassificationService to decouple relationship detection
from the classification system. Uses tag-based filtering instead of
classification lookups.
"""

import logging
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, select
from decimal import Decimal

from ..database.models import (
    Transaction, TransactionRelationship, Category,
    Tag, TransactionTag, Account
)

logger = logging.getLogger(__name__)


class RelationshipService:
    """Service for transaction relationship detection and management."""

    def __init__(self, db: Session):
        self.db = db

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

    def detect_transfer_pairs(
        self,
        date_tolerance_days: int = 3,
        amount_tolerance: Decimal = Decimal('0.01'),
        auto_link: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Detect potential transfer pairs (same amount, opposite types, within date range).

        Uses Category.category_type == 'Transfer' instead of classification codes.

        Args:
            date_tolerance_days: Maximum days between transactions (default: 3)
            amount_tolerance: Maximum amount difference to consider a match (default: 0.01)
            auto_link: If True, automatically create relationships for high-confidence matches

        Returns:
            List[Dict[str, Any]]: List of potential transfer pairs with confidence scores
        """
        # Get all unlinked transactions that could be transfers (by category type)
        transactions = (
            self.db.query(Transaction)
            .join(Category, Transaction.category_id == Category.category_id)
            .filter(Category.category_type == 'Transfer')
            .order_by(Transaction.transaction_date, Transaction.amount)
            .all()
        )

        # PERFORMANCE OPTIMIZATION: Fetch all existing relationships once
        existing_relationships = self.db.query(TransactionRelationship).all()
        linked_pairs = set()
        for rel in existing_relationships:
            linked_pairs.add((rel.transaction_id_1, rel.transaction_id_2))
            linked_pairs.add((rel.transaction_id_2, rel.transaction_id_1))

        potential_pairs = []
        processed_ids = set()

        for i, tx1 in enumerate(transactions):
            if tx1.transaction_id in processed_ids:
                continue

            for tx2 in transactions[i+1:]:
                if tx2.transaction_id in processed_ids:
                    continue

                if (tx1.transaction_id, tx2.transaction_id) in linked_pairs:
                    continue

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

                    if auto_link and match_score >= 0.8:
                        self.create_relationship(
                            tx1.transaction_id,
                            tx2.transaction_id,
                            pair_info['relationship_type'],
                            f"Auto-detected with {match_score:.0%} confidence"
                        )
                        processed_ids.add(tx1.transaction_id)
                        processed_ids.add(tx2.transaction_id)

        potential_pairs.sort(key=lambda x: x['confidence'], reverse=True)
        return potential_pairs

    def detect_credit_card_payments(
        self,
        date_tolerance_days: int = 5,
        auto_link: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Detect credit card payment/receipt pairs.

        Uses account type matching instead of classification codes.

        Args:
            date_tolerance_days: Maximum days between payment and receipt (default: 5)
            auto_link: If True, automatically create relationships for high-confidence matches

        Returns:
            List[Dict[str, Any]]: List of potential credit card payment pairs
        """
        # Get credit card accounts
        cc_account_ids = [
            a.account_id for a in
            self.db.query(Account.account_id).filter(Account.account_type == 'credit_card').all()
        ]

        if not cc_account_ids:
            return []

        # Get transfer-category transactions that involve credit card accounts
        # Payments: outgoing from non-CC account with matching amount
        # Receipts: incoming to CC account
        transfer_category_ids = [
            c.category_id for c in
            self.db.query(Category.category_id).filter(Category.category_type == 'Transfer').all()
        ]

        if not transfer_category_ids:
            return []

        # Payments from bank accounts (transfers out)
        payments = (
            self.db.query(Transaction)
            .filter(
                Transaction.category_id.in_(transfer_category_ids),
                ~Transaction.account_id.in_(cc_account_ids),
                Transaction.amount < 0  # outflows
            )
            .all()
        )

        # Receipts to credit card accounts (transfers in)
        receipts = (
            self.db.query(Transaction)
            .filter(
                Transaction.category_id.in_(transfer_category_ids),
                Transaction.account_id.in_(cc_account_ids),
                Transaction.amount > 0  # inflows
            )
            .all()
        )

        # PERFORMANCE OPTIMIZATION: Fetch all CC_PAYMENT_RECEIPT relationships once
        existing_relationships = self.db.query(TransactionRelationship).filter(
            TransactionRelationship.relationship_type == 'CC_PAYMENT_RECEIPT'
        ).all()
        linked_payment_ids = set()
        for rel in existing_relationships:
            linked_payment_ids.add(rel.transaction_id_1)
            linked_payment_ids.add(rel.transaction_id_2)

        potential_pairs = []

        for payment in payments:
            if payment.transaction_id in linked_payment_ids:
                continue

            for receipt in receipts:
                date_diff = abs((payment.transaction_date - receipt.transaction_date).days)
                if date_diff > date_tolerance_days:
                    continue

                # Check amount match (payment is negative, receipt is positive)
                amount_diff = abs(abs(payment.amount) - abs(receipt.amount))
                if amount_diff > Decimal('0.01'):
                    continue

                confidence = 1.0 - (date_diff / date_tolerance_days) * 0.3

                pair_info = {
                    'payment': payment,
                    'receipt': receipt,
                    'confidence': confidence,
                    'date_difference_days': date_diff,
                    'relationship_type': 'CC_PAYMENT_RECEIPT'
                }

                potential_pairs.append(pair_info)

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

        Uses tag-based filtering: looks for transactions tagged 'reimbursable'.

        Args:
            date_tolerance_days: Maximum days between expense and reimbursement (default: 30)
            auto_link: If True, automatically create relationships for high-confidence matches

        Returns:
            List[Dict[str, Any]]: List of potential reimbursement pairs
        """
        # Find reimbursable expenses via tag
        reimbursable_subq = (
            select(TransactionTag.transaction_id)
            .join(Tag, TransactionTag.tag_id == Tag.tag_id)
            .where(Tag.tag_name == 'reimbursable')
            .subquery()
        )

        expenses = self.db.query(Transaction).filter(
            Transaction.transaction_id.in_(select(reimbursable_subq)),
            Transaction.transaction_type == 'Expense'
        ).all()

        # Get income transactions that could be reimbursements
        reimbursements = self.db.query(Transaction).filter(
            Transaction.transaction_type == 'Income',
            Transaction.description.ilike('%reimburse%')
        ).all()

        # Also include any income tagged 'reimbursable'
        reimbursable_income = self.db.query(Transaction).filter(
            Transaction.transaction_id.in_(select(reimbursable_subq)),
            Transaction.transaction_type == 'Income'
        ).all()

        # Merge unique reimbursements
        reimb_ids = set()
        merged_reimbursements = []
        for r in reimbursements + reimbursable_income:
            if r.transaction_id not in reimb_ids:
                reimb_ids.add(r.transaction_id)
                merged_reimbursements.append(r)
        reimbursements = merged_reimbursements

        # PERFORMANCE OPTIMIZATION: Fetch all REIMBURSEMENT_PAIR relationships once
        existing_relationships = self.db.query(TransactionRelationship).filter(
            TransactionRelationship.relationship_type == 'REIMBURSEMENT_PAIR'
        ).all()
        linked_expense_ids = set()
        for rel in existing_relationships:
            linked_expense_ids.add(rel.transaction_id_1)
            linked_expense_ids.add(rel.transaction_id_2)

        potential_pairs = []

        for expense in expenses:
            if expense.transaction_id in linked_expense_ids:
                continue

            for reimbursement in reimbursements:
                if reimbursement.transaction_date < expense.transaction_date:
                    continue

                date_diff = (reimbursement.transaction_date - expense.transaction_date).days
                if date_diff > date_tolerance_days:
                    continue

                amount_diff = abs(expense.amount - reimbursement.amount)
                if amount_diff > Decimal('0.01'):
                    continue

                confidence = 1.0 - (date_diff / date_tolerance_days) * 0.4

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

        Uses description pattern matching for detection.

        Args:
            date_tolerance_days: Maximum days between dividend and reinvestment (default: 1)
            amount_tolerance: Maximum amount difference to consider a match (default: 0.01)
            auto_link: If True, automatically create relationships for high-confidence matches

        Returns:
            List[Dict[str, Any]]: List of potential dividend reinvestment pairs with confidence scores
        """
        # Get dividend income transactions by description pattern
        dividends = self.db.query(Transaction).filter(
            Transaction.transaction_type == 'Income',
            or_(
                Transaction.description.ilike('%dividend%'),
                Transaction.description.ilike('%distribution%'),
                Transaction.description.ilike('%div %'),
            )
        ).order_by(Transaction.transaction_date, Transaction.amount).all()

        # Get all potential reinvestment expense transactions
        reinvestments = self.db.query(Transaction).filter(
            Transaction.transaction_type == 'Expense',
            or_(
                Transaction.description.ilike('%reinvest%'),
                Transaction.description.ilike('%drip%'),
                Transaction.description.ilike('%auto reinvest%')
            )
        ).order_by(Transaction.transaction_date, Transaction.amount).all()

        # PERFORMANCE OPTIMIZATION: Fetch all existing relationships once
        existing_relationships = self.db.query(TransactionRelationship).all()
        linked_pairs = set()
        for rel in existing_relationships:
            linked_pairs.add((rel.transaction_id_1, rel.transaction_id_2))
            linked_pairs.add((rel.transaction_id_2, rel.transaction_id_1))

        potential_pairs = []
        processed_ids = set()

        for dividend in dividends:
            if dividend.transaction_id in processed_ids:
                continue

            for reinvestment in reinvestments:
                if reinvestment.transaction_id in processed_ids:
                    continue

                if (dividend.transaction_id, reinvestment.transaction_id) in linked_pairs:
                    continue

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

    # ==================== Helper Methods ====================

    def _calculate_transfer_match_score(
        self,
        tx1: Transaction,
        tx2: Transaction,
        date_tolerance_days: int,
        amount_tolerance: Decimal
    ) -> float:
        """Calculate match score for potential transfer pair."""
        amount_diff = abs(tx1.amount - tx2.amount)
        if amount_diff > amount_tolerance:
            return 0.0

        date_diff = abs((tx1.transaction_date - tx2.transaction_date).days)
        if date_diff > date_tolerance_days:
            return 0.0

        score = 0.6

        if amount_diff == 0:
            score += 0.2
        else:
            score += 0.2 * (1 - float(amount_diff / amount_tolerance))

        if date_diff == 0:
            score += 0.2
        else:
            score += 0.2 * (1 - date_diff / date_tolerance_days)

        if self._has_account_indicators(tx1, tx2):
            score = min(1.0, score + 0.1)

        if self._has_transfer_keywords(tx1) or self._has_transfer_keywords(tx2):
            score = min(1.0, score + 0.1)

        return min(1.0, score)

    def _determine_relationship_type(
        self,
        tx1: Transaction,
        tx2: Transaction
    ) -> str:
        """Determine the type of relationship between two transactions."""
        # Check tags for hints
        tx1_tags = {t.tag_name for t in tx1.tags} if tx1.tags else set()
        tx2_tags = {t.tag_name for t in tx2.tags} if tx2.tags else set()

        if 'reimbursable' in tx1_tags or 'reimbursable' in tx2_tags:
            return 'REIMBURSEMENT_PAIR'

        # Check if one involves a credit card account
        if tx1.account and tx2.account:
            account_types = {
                getattr(tx1.account, 'account_type', None),
                getattr(tx2.account, 'account_type', None)
            }
            if 'credit_card' in account_types:
                return 'CC_PAYMENT_RECEIPT'

        return 'TRANSFER_PAIR'

    def _has_account_indicators(
        self,
        tx1: Transaction,
        tx2: Transaction
    ) -> bool:
        """Check if transactions have account indicators suggesting they're related."""
        if tx1.transfer_account_from and tx2.transfer_account_to:
            if tx1.transfer_account_from == tx2.transfer_account_to:
                return True

        if tx1.transfer_account_to and tx2.transfer_account_from:
            if tx1.transfer_account_to == tx2.transfer_account_from:
                return True

        if tx1.source and tx2.source:
            words1 = set(tx1.source.lower().split())
            words2 = set(tx2.source.lower().split())
            common_words = words1.intersection(words2)

            account_keywords = {'checking', 'savings', 'credit', 'card', 'account'}
            if common_words.intersection(account_keywords):
                return True

        return False

    def _has_transfer_keywords(
        self,
        tx: Transaction
    ) -> bool:
        """Check if transaction description contains transfer keywords."""
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
        """Calculate similarity between two descriptions."""
        if not desc1 or not desc2:
            return 0.0

        words1 = set(desc1.lower().split())
        words2 = set(desc2.lower().split())

        if not words1 or not words2:
            return 0.0

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
        """Calculate match score for potential dividend reinvestment pair."""
        amount_diff = abs(dividend.amount - reinvestment.amount)
        if amount_diff > amount_tolerance:
            return 0.0

        date_diff = abs((dividend.transaction_date - reinvestment.transaction_date).days)
        if date_diff > date_tolerance_days:
            return 0.0

        score = 0.6

        if amount_diff == 0:
            score += 0.2
        else:
            score += 0.2 * (1 - float(amount_diff / amount_tolerance))

        if date_diff == 0:
            score += 0.2
        elif date_diff == 1:
            score += 0.1

        if dividend.description and reinvestment.description:
            desc_similarity = self._calculate_description_similarity(
                dividend.description, reinvestment.description
            )
            if desc_similarity >= 0.5:
                score = min(1.0, score + 0.1)

        if dividend.source and reinvestment.source and dividend.source == reinvestment.source:
            score = min(1.0, score + 0.1)

        return min(1.0, score)
