"""Entity CRUD service."""

from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..database.models import Entity, Account


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
