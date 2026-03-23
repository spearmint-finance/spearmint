"""Category CRUD service."""

from typing import Optional, List, Dict
import re
from sqlalchemy.orm import Session
from sqlalchemy import or_

from ..database.models import Category, CategoryRule, Transaction, TransactionSplit, Budget
from ..utils.validators import DataValidator, ValidationError


class CategoryService:
    """Service for category CRUD operations."""
    
    VALID_CATEGORY_TYPES = {'Income', 'Expense', 'Transfer', 'Both'}
    
    def __init__(self, db: Session):
        """
        Initialize category service.
        
        Args:
            db: Database session
        """
        self.db = db
        self.validator = DataValidator()
    
    def create_category(
        self,
        category_name: str,
        category_type: str,
        parent_category_id: Optional[int] = None,
        description: Optional[str] = None,
        entity_id: Optional[int] = None,
    ) -> Category:
        """
        Create a new category.

        Args:
            category_name: Name of the category
            category_type: 'Income', 'Expense', 'Transfer', or 'Both'
            parent_category_id: Parent category ID for hierarchical categories
            description: Category description

        Returns:
            Category: Created category
            
        Raises:
            ValidationError: If validation fails
        """
        # Validate inputs
        category_name = self.validator.validate_category(category_name, 'Category Name')
        
        if category_type not in self.VALID_CATEGORY_TYPES:
            raise ValidationError(
                f"Category type must be one of {self.VALID_CATEGORY_TYPES}, got '{category_type}'"
            )
        
        # Check for duplicate name within same entity scope
        dup_query = self.db.query(Category).filter(
            Category.category_name == category_name
        )
        if entity_id:
            dup_query = dup_query.filter(Category.entity_id == entity_id)
        else:
            dup_query = dup_query.filter(Category.entity_id.is_(None))
        existing = dup_query.first()
        if existing:
            scope = "global" if not entity_id else f"entity {entity_id}"
            raise ValidationError(f"Category '{category_name}' already exists in {scope} scope")
        
        # Verify parent category if provided
        if parent_category_id:
            parent = self.db.query(Category).filter(
                Category.category_id == parent_category_id
            ).first()
            if not parent:
                raise ValidationError(f"Parent category with ID {parent_category_id} not found")
            
            # Ensure parent and child have compatible types
            if parent.category_type != 'Both' and category_type != 'Both':
                if parent.category_type != category_type:
                    raise ValidationError(
                        f"Child category type '{category_type}' incompatible with "
                        f"parent category type '{parent.category_type}'"
                    )
        
        # Create category
        category = Category(
            category_name=category_name,
            category_type=category_type,
            parent_category_id=parent_category_id,
            description=description,
            entity_id=entity_id,
        )
        
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        
        return category
    
    def get_category(self, category_id: int) -> Optional[Category]:
        """
        Get category by ID.
        
        Args:
            category_id: Category ID
            
        Returns:
            Optional[Category]: Category if found, None otherwise
        """
        return self.db.query(Category).filter(
            Category.category_id == category_id
        ).first()
    
    def get_category_by_name(self, category_name: str) -> Optional[Category]:
        """
        Get category by name.
        
        Args:
            category_name: Category name
            
        Returns:
            Optional[Category]: Category if found, None otherwise
        """
        return self.db.query(Category).filter(
            Category.category_name == category_name
        ).first()
    
    def list_categories(
        self,
        category_type: Optional[str] = None,
        parent_category_id: Optional[int] = None,
        include_transfer_categories: bool = True,
        search_text: Optional[str] = None,
        entity_id: Optional[int] = None,
    ) -> List[Category]:
        """
        List categories with optional filters.
        
        Args:
            category_type: Filter by category type
            parent_category_id: Filter by parent category (None for root categories)
            include_transfer_categories: Whether to include transfer categories
            search_text: Search in category name or description
            
        Returns:
            List[Category]: List of categories
        """
        query = self.db.query(Category)
        
        # Apply filters
        if category_type:
            if category_type not in self.VALID_CATEGORY_TYPES:
                raise ValidationError(
                    f"Category type must be one of {self.VALID_CATEGORY_TYPES}, got '{category_type}'"
                )
            query = query.filter(
                or_(
                    Category.category_type == category_type,
                    Category.category_type == 'Both'
                )
            )
        
        if parent_category_id is not None:
            query = query.filter(Category.parent_category_id == parent_category_id)
        
        if not include_transfer_categories:
            query = query.filter(Category.category_type != 'Transfer')
        
        if search_text:
            search_pattern = f"%{search_text}%"
            query = query.filter(
                or_(
                    Category.category_name.ilike(search_pattern),
                    Category.description.ilike(search_pattern)
                )
            )

        if entity_id is not None:
            # Show entity-specific categories + global categories (entity_id IS NULL)
            query = query.filter(
                or_(
                    Category.entity_id == entity_id,
                    Category.entity_id.is_(None)
                )
            )

        return query.order_by(Category.category_name).all()
    
    def get_root_categories(self, category_type: Optional[str] = None) -> List[Category]:
        """
        Get root categories (categories without parent).
        
        Args:
            category_type: Filter by category type
            
        Returns:
            List[Category]: List of root categories
        """
        return self.list_categories(
            category_type=category_type,
            parent_category_id=None
        )
    
    def get_child_categories(self, parent_category_id: int) -> List[Category]:
        """
        Get child categories of a parent category.
        
        Args:
            parent_category_id: Parent category ID
            
        Returns:
            List[Category]: List of child categories
        """
        return self.list_categories(parent_category_id=parent_category_id)
    
    def update_category(
        self,
        category_id: int,
        **updates
    ) -> Optional[Category]:
        """
        Update category.
        
        Args:
            category_id: Category ID
            **updates: Fields to update
            
        Returns:
            Optional[Category]: Updated category if found, None otherwise
            
        Raises:
            ValidationError: If validation fails
        """
        category = self.get_category(category_id)
        if not category:
            return None
        
        # Validate updates
        if 'category_name' in updates:
            new_name = self.validator.validate_category(updates['category_name'], 'Category Name')
            # Check for duplicate name within same entity scope (excluding current category)
            entity_id = updates.get('entity_id', category.entity_id)
            dup_query = self.db.query(Category).filter(
                Category.category_name == new_name,
                Category.category_id != category_id
            )
            if entity_id:
                dup_query = dup_query.filter(Category.entity_id == entity_id)
            else:
                dup_query = dup_query.filter(Category.entity_id.is_(None))
            existing = dup_query.first()
            if existing:
                scope = "global" if not entity_id else f"entity {entity_id}"
                raise ValidationError(f"Category '{new_name}' already exists in {scope} scope")
            updates['category_name'] = new_name
        
        if 'category_type' in updates:
            if updates['category_type'] not in self.VALID_CATEGORY_TYPES:
                raise ValidationError(
                    f"Category type must be one of {self.VALID_CATEGORY_TYPES}, "
                    f"got '{updates['category_type']}'"
                )
        
        if 'parent_category_id' in updates:
            parent_id = updates['parent_category_id']
            if parent_id:
                # Prevent circular reference
                if parent_id == category_id:
                    raise ValidationError("Category cannot be its own parent")
                
                # Verify parent exists
                parent = self.get_category(parent_id)
                if not parent:
                    raise ValidationError(f"Parent category with ID {parent_id} not found")
                
                # Check if this would create a circular reference
                if self._would_create_circular_reference(category_id, parent_id):
                    raise ValidationError("Cannot set parent: would create circular reference")
        
        # Update fields
        for key, value in updates.items():
            if hasattr(category, key):
                setattr(category, key, value)
        
        self.db.commit()
        self.db.refresh(category)
        
        return category
    
    def delete_category(self, category_id: int, force: bool = False) -> bool:
        """
        Delete category.
        
        Args:
            category_id: Category ID
            force: If True, delete even if category has transactions or children
            
        Returns:
            bool: True if deleted, False if not found
            
        Raises:
            ValidationError: If category has transactions or children and force=False
        """
        category = self.get_category(category_id)
        if not category:
            return False
        
        if not force:
            # Check for child categories
            children = self.get_child_categories(category_id)
            if children:
                raise ValidationError(
                    f"Cannot delete category: has {len(children)} child categories. "
                    "Use force=True to delete anyway."
                )
            
            # Check for transactions
            from ..database.models import Transaction
            transaction_count = self.db.query(Transaction).filter(
                Transaction.category_id == category_id
            ).count()
            if transaction_count > 0:
                raise ValidationError(
                    f"Cannot delete category: has {transaction_count} transactions. "
                    "Use force=True to delete anyway."
                )
        
        # Delete category
        self.db.delete(category)
        self.db.commit()
        
        return True
    
    def merge_category(self, source_id: int, target_id: int) -> dict:
        """
        Merge source category into target. Reassigns all transactions, splits,
        rules, budgets, and child categories from source to target, then deletes source.

        Returns:
            dict with counts of reassigned items
        """
        source = self.get_category(source_id)
        if not source:
            raise ValidationError(f"Source category {source_id} not found")

        target = self.get_category(target_id)
        if not target:
            raise ValidationError(f"Target category {target_id} not found")

        if source_id == target_id:
            raise ValidationError("Cannot merge a category into itself")

        # Reassign transactions
        tx_count = self.db.query(Transaction).filter(
            Transaction.category_id == source_id
        ).update({Transaction.category_id: target_id})

        # Reassign splits
        split_count = self.db.query(TransactionSplit).filter(
            TransactionSplit.category_id == source_id
        ).update({TransactionSplit.category_id: target_id})

        # Reassign category rules
        rule_count = self.db.query(CategoryRule).filter(
            CategoryRule.category_id == source_id
        ).update({CategoryRule.category_id: target_id})

        # Reassign budgets
        budget_count = self.db.query(Budget).filter(
            Budget.category_id == source_id
        ).update({Budget.category_id: target_id})

        # Reparent child categories
        child_count = self.db.query(Category).filter(
            Category.parent_category_id == source_id
        ).update({Category.parent_category_id: target_id})

        # Delete the now-empty source category
        self.db.delete(source)
        self.db.commit()

        return {
            "transactions": tx_count,
            "splits": split_count,
            "rules": rule_count,
            "budgets": budget_count,
            "children": child_count,
        }

    def _would_create_circular_reference(self, category_id: int, new_parent_id: int) -> bool:
        """
        Check if setting a new parent would create a circular reference.
        
        Args:
            category_id: Category ID
            new_parent_id: Proposed new parent ID
            
        Returns:
            bool: True if would create circular reference
        """
        # Walk up the parent chain from new_parent_id
        current_id = new_parent_id
        visited = set()
        
        while current_id:
            if current_id == category_id:
                return True  # Circular reference detected
            
            if current_id in visited:
                break  # Already visited, avoid infinite loop
            
            visited.add(current_id)
            
            parent = self.get_category(current_id)
            if not parent:
                break
            
            current_id = parent.parent_category_id

        return False

    # ========================================================================
    # Category Rule Methods
    # ========================================================================

    def create_category_rule(
        self,
        rule_name: str,
        category_id: Optional[int] = None,
        entity_id: Optional[int] = None,
        rule_priority: int = 100,
        is_active: bool = True,
        description_pattern: Optional[str] = None,
        source_pattern: Optional[str] = None,
        amount_min: Optional[float] = None,
        amount_max: Optional[float] = None,
        payment_method_pattern: Optional[str] = None,
        transaction_type_pattern: Optional[str] = None
    ) -> CategoryRule:
        """
        Create a new category/entity assignment rule.

        A rule can assign a category, an entity, or both to matching transactions.
        At least one of category_id or entity_id must be provided.
        """
        # Validate at least one assignment target
        if not category_id and not entity_id:
            raise ValidationError("At least one of category_id or entity_id must be provided")

        # Validate category exists if provided
        if category_id:
            category = self.get_category(category_id)
            if not category:
                raise ValidationError(f"Category with ID {category_id} not found")

        # Validate entity exists if provided
        if entity_id:
            from ..database.models import Entity
            entity = self.db.query(Entity).filter(Entity.entity_id == entity_id).first()
            if not entity:
                raise ValidationError(f"Entity with ID {entity_id} not found")

        # Validate transaction type pattern if provided
        if transaction_type_pattern and transaction_type_pattern not in ('Income', 'Expense'):
            raise ValidationError(
                f"Transaction type pattern must be 'Income' or 'Expense', got '{transaction_type_pattern}'"
            )

        # Validate at least one pattern is provided
        if not any([description_pattern, source_pattern, payment_method_pattern,
                   amount_min is not None, amount_max is not None, transaction_type_pattern]):
            raise ValidationError("At least one matching criterion must be provided")

        # Create rule
        rule = CategoryRule(
            rule_name=rule_name,
            category_id=category_id,
            entity_id=entity_id,
            rule_priority=rule_priority,
            is_active=is_active,
            description_pattern=description_pattern,
            source_pattern=source_pattern,
            amount_min=amount_min,
            amount_max=amount_max,
            payment_method_pattern=payment_method_pattern,
            transaction_type_pattern=transaction_type_pattern
        )

        self.db.add(rule)
        self.db.commit()
        self.db.refresh(rule)

        return rule

    def get_category_rule(self, rule_id: int) -> Optional[CategoryRule]:
        """
        Get category rule by ID.

        Args:
            rule_id: Rule ID

        Returns:
            Optional[CategoryRule]: Rule if found, None otherwise
        """
        return self.db.query(CategoryRule).filter(
            CategoryRule.rule_id == rule_id
        ).first()

    def list_category_rules(
        self,
        active_only: bool = False,
        category_id: Optional[int] = None
    ) -> List[CategoryRule]:
        """
        List category rules with optional filters.

        Args:
            active_only: Only return active rules
            category_id: Filter by category

        Returns:
            List[CategoryRule]: List of rules
        """
        query = self.db.query(CategoryRule)

        if active_only:
            query = query.filter(CategoryRule.is_active == True)

        if category_id is not None:
            query = query.filter(CategoryRule.category_id == category_id)

        return query.order_by(CategoryRule.rule_priority).all()

    def update_category_rule(
        self,
        rule_id: int,
        **updates
    ) -> Optional[CategoryRule]:
        """
        Update category rule.

        Args:
            rule_id: Rule ID
            **updates: Fields to update

        Returns:
            Optional[CategoryRule]: Updated rule if found, None otherwise

        Raises:
            ValidationError: If validation fails
        """
        rule = self.get_category_rule(rule_id)
        if not rule:
            return None

        # Validate category if being updated
        if 'category_id' in updates and updates['category_id']:
            category = self.get_category(updates['category_id'])
            if not category:
                raise ValidationError(f"Category with ID {updates['category_id']} not found")

        # Validate entity if being updated
        if 'entity_id' in updates and updates['entity_id']:
            from ..database.models import Entity
            entity = self.db.query(Entity).filter(Entity.entity_id == updates['entity_id']).first()
            if not entity:
                raise ValidationError(f"Entity with ID {updates['entity_id']} not found")

        # Validate transaction type pattern if being updated
        if 'transaction_type_pattern' in updates:
            pattern = updates['transaction_type_pattern']
            if pattern and pattern not in ('Income', 'Expense'):
                raise ValidationError(
                    f"Transaction type pattern must be 'Income' or 'Expense', got '{pattern}'"
                )

        # Update fields
        for key, value in updates.items():
            if hasattr(rule, key):
                setattr(rule, key, value)

        self.db.commit()
        self.db.refresh(rule)

        return rule

    def delete_category_rule(self, rule_id: int) -> bool:
        """
        Delete category rule.

        Args:
            rule_id: Rule ID

        Returns:
            bool: True if deleted, False if not found
        """
        rule = self.get_category_rule(rule_id)
        if not rule:
            return False

        self.db.delete(rule)
        self.db.commit()

        return True

    def auto_categorize_transaction(self, transaction: Transaction) -> bool:
        """
        Automatically apply rules to a transaction (category and/or entity).

        Args:
            transaction: Transaction to process

        Returns:
            bool: True if any assignment was applied
        """
        # Get active rules ordered by priority
        rules = self.db.query(CategoryRule).filter(
            CategoryRule.is_active == True
        ).order_by(CategoryRule.rule_priority).all()

        for rule in rules:
            if self._rule_matches(transaction, rule):
                applied = False
                if rule.category_id:
                    transaction.category_id = rule.category_id
                    applied = True
                if rule.entity_id:
                    transaction.entity_id = rule.entity_id
                    applied = True
                return applied

        return False

    def _rule_matches(self, transaction: Transaction, rule: CategoryRule) -> bool:
        """
        Check if a transaction matches a category rule.

        Args:
            transaction: Transaction to check
            rule: Category rule

        Returns:
            bool: True if transaction matches rule
        """
        # Check transaction type pattern
        if rule.transaction_type_pattern:
            if transaction.transaction_type != rule.transaction_type_pattern:
                return False

        # Check description pattern
        if rule.description_pattern:
            if not transaction.description:
                return False
            pattern = rule.description_pattern.replace('%', '.*')
            if not re.search(pattern, transaction.description, re.IGNORECASE):
                return False

        # Check source pattern
        if rule.source_pattern:
            if not transaction.source:
                return False
            pattern = rule.source_pattern.replace('%', '.*')
            if not re.search(pattern, transaction.source, re.IGNORECASE):
                return False

        # Check amount range
        if rule.amount_min is not None and transaction.amount < rule.amount_min:
            return False

        if rule.amount_max is not None and transaction.amount > rule.amount_max:
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

    def test_category_rule(
        self,
        description_pattern: Optional[str] = None,
        source_pattern: Optional[str] = None,
        amount_min: Optional[float] = None,
        amount_max: Optional[float] = None,
        payment_method_pattern: Optional[str] = None,
        transaction_type_pattern: Optional[str] = None,
        limit: int = 10
    ) -> Dict:
        """
        Test a category rule against existing transactions.

        Args:
            description_pattern: Pattern to match in description
            source_pattern: Pattern to match in source
            amount_min: Minimum amount
            amount_max: Maximum amount
            payment_method_pattern: Pattern to match in payment method
            transaction_type_pattern: 'Income', 'Expense', or None
            limit: Maximum number of matching transactions to return

        Returns:
            Dict: Test results with matching transactions and count
        """
        # Create a temporary rule object for testing
        temp_rule = CategoryRule(
            rule_name="Test Rule",
            category_id=1,  # Dummy value
            description_pattern=description_pattern,
            source_pattern=source_pattern,
            amount_min=amount_min,
            amount_max=amount_max,
            payment_method_pattern=payment_method_pattern,
            transaction_type_pattern=transaction_type_pattern
        )

        # Get all transactions
        transactions = self.db.query(Transaction).all()

        # Find matching transactions
        matching_transactions = []
        for transaction in transactions:
            if self._rule_matches(transaction, temp_rule):
                matching_transactions.append(transaction)
                if len(matching_transactions) >= limit:
                    break

        return {
            'total_matches': len(matching_transactions),
            'sample_transactions': matching_transactions[:limit],
            'has_more': len(matching_transactions) > limit
        }

    def apply_category_rules(
        self,
        transaction_ids: Optional[List[int]] = None,
        rule_ids: Optional[List[int]] = None,
        force_recategorize: bool = False
    ) -> Dict:
        """
        Apply category rules to transactions.

        Args:
            transaction_ids: Specific transaction IDs to process (None = all)
            rule_ids: Specific rule IDs to apply (None = all active rules)
            force_recategorize: If True, recategorize even if already categorized

        Returns:
            Dict: Statistics about categorization
        """
        # Get rules to apply
        if rule_ids:
            rules = self.db.query(CategoryRule).filter(
                CategoryRule.rule_id.in_(rule_ids)
            ).order_by(CategoryRule.rule_priority).all()
        else:
            rules = self.db.query(CategoryRule).filter(
                CategoryRule.is_active == True
            ).order_by(CategoryRule.rule_priority).all()

        # Get transactions to process
        query = self.db.query(Transaction)
        if transaction_ids:
            query = query.filter(Transaction.transaction_id.in_(transaction_ids))

        transactions = query.all()

        categorized_count = 0
        entity_assigned_count = 0
        skipped_count = 0

        for transaction in transactions:
            # Skip if already fully assigned and not forcing
            if transaction.category_id and transaction.entity_id and not force_recategorize:
                skipped_count += 1
                continue

            # Try to match with rules
            matched = False
            for rule in rules:
                if self._rule_matches(transaction, rule):
                    if rule.category_id and (not transaction.category_id or force_recategorize):
                        transaction.category_id = rule.category_id
                        categorized_count += 1
                    if rule.entity_id and (not transaction.entity_id or force_recategorize):
                        transaction.entity_id = rule.entity_id
                        entity_assigned_count += 1
                    matched = True
                    break  # Stop at first matching rule

            if not matched:
                skipped_count += 1

        self.db.commit()

        return {
            'total_processed': len(transactions),
            'categorized_count': categorized_count,
            'entity_assigned_count': entity_assigned_count,
            'skipped_count': skipped_count,
            'rules_applied': len(rules)
        }

