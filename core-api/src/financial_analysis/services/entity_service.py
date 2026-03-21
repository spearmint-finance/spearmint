"""Entity CRUD service."""

from datetime import date
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, case, and_

from ..database.models import Entity, Account, Transaction, Category


class EntityService:
    """Service for entity management."""

    def __init__(self, db: Session):
        self.db = db

    def create_entity(
        self,
        entity_name: str,
        entity_type: str,
        tax_id: Optional[str] = None,
        address: Optional[str] = None,
        fiscal_year_start_month: int = 1,
        is_default: bool = False,
        notes: Optional[str] = None,
    ) -> Entity:
        """Create a new entity."""
        # If this is set as default, unset any existing default
        if is_default:
            self.db.query(Entity).filter(Entity.is_default == True).update(
                {"is_default": False}
            )

        entity = Entity(
            entity_name=entity_name,
            entity_type=entity_type,
            tax_id=tax_id,
            address=address,
            fiscal_year_start_month=fiscal_year_start_month,
            is_default=is_default,
            notes=notes,
        )
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def get_entity(self, entity_id: int) -> Optional[Entity]:
        """Get entity by ID."""
        return self.db.query(Entity).filter(Entity.entity_id == entity_id).first()

    def list_entities(self) -> List[Entity]:
        """List all entities, default first."""
        return (
            self.db.query(Entity)
            .order_by(Entity.is_default.desc(), Entity.entity_name.asc())
            .all()
        )

    def update_entity(self, entity_id: int, **updates) -> Optional[Entity]:
        """Update an entity."""
        entity = self.get_entity(entity_id)
        if not entity:
            return None

        # If setting as default, unset any existing default
        if updates.get("is_default"):
            self.db.query(Entity).filter(
                Entity.is_default == True,
                Entity.entity_id != entity_id,
            ).update({"is_default": False})

        for key, value in updates.items():
            if value is not None and hasattr(entity, key):
                setattr(entity, key, value)

        self.db.commit()
        self.db.refresh(entity)
        return entity

    def delete_entity(self, entity_id: int) -> bool:
        """Delete an entity. Fails if accounts are still assigned."""
        entity = self.get_entity(entity_id)
        if not entity:
            return False

        if entity.is_default:
            raise ValueError("Cannot delete the default entity")

        # Check for assigned accounts
        account_count = (
            self.db.query(func.count(Account.account_id))
            .filter(Account.entity_id == entity_id)
            .scalar()
        )
        if account_count > 0:
            raise ValueError(
                f"Cannot delete entity with {account_count} assigned account(s). "
                "Reassign or remove accounts first."
            )

        self.db.delete(entity)
        self.db.commit()
        return True

    def get_account_count(self, entity_id: int) -> int:
        """Get number of accounts assigned to an entity."""
        return (
            self.db.query(func.count(Account.account_id))
            .filter(Account.entity_id == entity_id)
            .scalar()
        )

    def ensure_default_entity(self) -> Entity:
        """Ensure a default 'Personal' entity exists. Create if missing."""
        default = (
            self.db.query(Entity).filter(Entity.is_default == True).first()
        )
        if default:
            return default

        return self.create_entity(
            entity_name="Personal",
            entity_type="personal",
            is_default=True,
        )

    # ==================== Financial Statements ====================

    def get_pnl(
        self, entity_id: int, start_date: date, end_date: date
    ) -> Dict[str, Any]:
        """
        Generate a Profit & Loss statement for an entity over a date range.

        Returns revenue and expenses broken down by category, with totals.
        """
        entity = self.get_entity(entity_id)
        if not entity:
            raise ValueError(f"Entity {entity_id} not found")

        # Get entity's account IDs
        account_ids = [
            a.account_id
            for a in self.db.query(Account.account_id)
            .filter(Account.entity_id == entity_id)
            .all()
        ]

        if not account_ids:
            return self._empty_pnl(entity, start_date, end_date)

        # Query income and expense by category
        rows = (
            self.db.query(
                Transaction.transaction_type,
                Category.category_id,
                Category.category_name,
                func.sum(func.abs(Transaction.amount)).label("total"),
            )
            .join(Category, Transaction.category_id == Category.category_id)
            .filter(
                and_(
                    Transaction.account_id.in_(account_ids),
                    Transaction.transaction_date >= start_date,
                    Transaction.transaction_date <= end_date,
                    Transaction.include_in_analysis == True,
                )
            )
            .group_by(
                Transaction.transaction_type,
                Category.category_id,
                Category.category_name,
            )
            .order_by(func.sum(func.abs(Transaction.amount)).desc())
            .all()
        )

        revenue_items = []
        expense_items = []
        total_revenue = 0.0
        total_expenses = 0.0

        for row in rows:
            item = {
                "category_name": row.category_name,
                "category_id": row.category_id,
                "amount": float(row.total),
            }
            if row.transaction_type == "Income":
                revenue_items.append(item)
                total_revenue += float(row.total)
            else:
                expense_items.append(item)
                total_expenses += float(row.total)

        return {
            "entity_id": entity.entity_id,
            "entity_name": entity.entity_name,
            "period": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat(),
            },
            "revenue": {
                "total": total_revenue,
                "by_category": revenue_items,
            },
            "expenses": {
                "total": total_expenses,
                "by_category": expense_items,
            },
            "net_income": total_revenue - total_expenses,
        }

    def get_cashflow(
        self, entity_id: int, start_date: date, end_date: date
    ) -> Dict[str, Any]:
        """
        Generate a Cash Flow statement for an entity over a date range.

        Classifies transactions into operating, investing, and financing
        based on transaction classifications and category patterns.
        """
        entity = self.get_entity(entity_id)
        if not entity:
            raise ValueError(f"Entity {entity_id} not found")

        account_ids = [
            a.account_id
            for a in self.db.query(Account.account_id)
            .filter(Account.entity_id == entity_id)
            .all()
        ]

        if not account_ids:
            return self._empty_cashflow(entity, start_date, end_date)

        # Get all transactions for the period
        transactions = (
            self.db.query(Transaction)
            .filter(
                and_(
                    Transaction.account_id.in_(account_ids),
                    Transaction.transaction_date >= start_date,
                    Transaction.transaction_date <= end_date,
                )
            )
            .all()
        )

        # Classify into operating / investing / financing
        operating_items = []
        investing_items = []
        financing_items = []

        for tx in transactions:
            amount = float(tx.amount)
            if tx.transaction_type == "Expense":
                amount = -abs(amount)

            category_name = ""
            if tx.category_id:
                cat = self.db.query(Category).filter(
                    Category.category_id == tx.category_id
                ).first()
                if cat:
                    category_name = cat.category_name

            item = {
                "description": tx.description or category_name or "Uncategorized",
                "amount": amount,
                "category_name": category_name,
            }

            # Classification heuristic using tags:
            # - Transfers and loan payments → financing
            # - Capital expenses (tagged 'capital-expense') → investing
            # - Everything else → operating
            if tx.category and tx.category.category_type == 'Transfer':
                financing_items.append(item)
            elif tx.is_capital_expense:
                investing_items.append(item)
            else:
                operating_items.append(item)

        operating_total = sum(i["amount"] for i in operating_items)
        investing_total = sum(i["amount"] for i in investing_items)
        financing_total = sum(i["amount"] for i in financing_items)

        # Aggregate operating items by category for cleaner display
        operating_by_cat: Dict[str, float] = {}
        for item in operating_items:
            key = item["category_name"] or "Uncategorized"
            operating_by_cat[key] = operating_by_cat.get(key, 0) + item["amount"]

        operating_summary = [
            {"description": k, "amount": v}
            for k, v in sorted(operating_by_cat.items(), key=lambda x: -abs(x[1]))
        ]

        return {
            "entity_id": entity.entity_id,
            "entity_name": entity.entity_name,
            "period": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat(),
            },
            "operating": {
                "net_income": operating_total,
                "items": operating_summary,
                "total": operating_total,
            },
            "investing": {
                "items": self._aggregate_items(investing_items),
                "total": investing_total,
            },
            "financing": {
                "items": self._aggregate_items(financing_items),
                "total": financing_total,
            },
            "net_change": operating_total + investing_total + financing_total,
        }

    def _aggregate_items(self, items: list) -> list:
        """Aggregate items by category for cleaner display."""
        by_cat: Dict[str, float] = {}
        for item in items:
            key = item.get("category_name") or item.get("description", "Other")
            by_cat[key] = by_cat.get(key, 0) + item["amount"]
        return [
            {"description": k, "amount": v}
            for k, v in sorted(by_cat.items(), key=lambda x: -abs(x[1]))
        ]

    def _empty_pnl(self, entity, start_date, end_date):
        return {
            "entity_id": entity.entity_id,
            "entity_name": entity.entity_name,
            "period": {"start": start_date.isoformat(), "end": end_date.isoformat()},
            "revenue": {"total": 0, "by_category": []},
            "expenses": {"total": 0, "by_category": []},
            "net_income": 0,
        }

    def _empty_cashflow(self, entity, start_date, end_date):
        return {
            "entity_id": entity.entity_id,
            "entity_name": entity.entity_name,
            "period": {"start": start_date.isoformat(), "end": end_date.isoformat()},
            "operating": {"net_income": 0, "items": [], "total": 0},
            "investing": {"items": [], "total": 0},
            "financing": {"items": [], "total": 0},
            "net_change": 0,
        }
