"""Data validation utilities for financial analysis tool."""

from datetime import datetime, date
from decimal import Decimal, InvalidOperation
from typing import Optional, Tuple, Any
import re


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


class DataValidator:
    """Validator class for transaction data."""
    
    VALID_TRANSACTION_TYPES = {'Income', 'Expense'}
    VALID_IMPORT_MODES = {'full', 'incremental', 'update'}
    
    @staticmethod
    def validate_date(value: Any, field_name: str = "Date") -> date:
        """
        Validate date field.
        
        Args:
            value: Date value to validate (can be string, datetime, or date)
            field_name: Name of the field for error messages
            
        Returns:
            date: Validated date object
            
        Raises:
            ValidationError: If date is invalid or in the future
        """
        if value is None:
            raise ValidationError(f"{field_name} is required")
        
        # Convert to date if needed
        if isinstance(value, str):
            try:
                # Check if this is a "Month" column value (e.g., "10/1/2025" representing October 2025)
                # These always have day=1, so we'll treat them as the first of the month
                if '/' in value and value.count('/') == 2:
                    parts = value.split('/')
                    if len(parts) == 3 and parts[1] == '1':
                        # This looks like a month format (MM/1/YYYY), use it as-is
                        pass

                # Try common date formats
                for fmt in ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%Y/%m/%d', '%m/1/%Y']:
                    try:
                        parsed_date = datetime.strptime(value, fmt).date()
                        break
                    except ValueError:
                        continue
                else:
                    raise ValidationError(f"{field_name} has invalid format: {value}")
            except Exception as e:
                raise ValidationError(f"{field_name} is invalid: {str(e)}")
        elif isinstance(value, datetime):
            parsed_date = value.date()
        elif isinstance(value, date):
            parsed_date = value
        else:
            raise ValidationError(f"{field_name} must be a date, got {type(value)}")
        
        # Check if date is not in the future
        if parsed_date > date.today():
            raise ValidationError(f"{field_name} cannot be in the future: {parsed_date}")
        
        return parsed_date
    
    @staticmethod
    def validate_amount(value: Any, field_name: str = "Amount", allow_zero: bool = False) -> Decimal:
        """
        Validate amount field.
        
        Args:
            value: Amount value to validate
            field_name: Name of the field for error messages
            allow_zero: Whether to allow zero values
            
        Returns:
            Decimal: Validated amount
            
        Raises:
            ValidationError: If amount is invalid or zero (when not allowed)
        """
        if value is None:
            raise ValidationError(f"{field_name} is required")
        
        try:
            # Convert to Decimal for precise financial calculations
            if isinstance(value, str):
                # Remove currency symbols and commas
                cleaned = re.sub(r'[,$£€¥]', '', value.strip())
                amount = Decimal(cleaned)
            elif isinstance(value, (int, float)):
                amount = Decimal(str(value))
            elif isinstance(value, Decimal):
                amount = value
            else:
                raise ValidationError(f"{field_name} must be numeric, got {type(value)}")
        except (InvalidOperation, ValueError) as e:
            raise ValidationError(f"{field_name} is not a valid number: {value}")
        
        # Check for zero
        if not allow_zero and amount == 0:
            raise ValidationError(f"{field_name} cannot be zero")
        
        return amount
    
    @staticmethod
    def validate_transaction_type(value: Any, field_name: str = "Type") -> str:
        """
        Validate transaction type field.
        
        Args:
            value: Transaction type to validate
            field_name: Name of the field for error messages
            
        Returns:
            str: Validated transaction type
            
        Raises:
            ValidationError: If type is invalid
        """
        if value is None or (isinstance(value, str) and not value.strip()):
            raise ValidationError(f"{field_name} is required")
        
        value_str = str(value).strip()
        
        # Case-insensitive comparison
        for valid_type in DataValidator.VALID_TRANSACTION_TYPES:
            if value_str.lower() == valid_type.lower():
                return valid_type  # Return the canonical form
        
        raise ValidationError(
            f"{field_name} must be one of {DataValidator.VALID_TRANSACTION_TYPES}, got '{value_str}'"
        )
    
    @staticmethod
    def validate_category(value: Any, field_name: str = "Category") -> str:
        """
        Validate category field.
        
        Args:
            value: Category value to validate
            field_name: Name of the field for error messages
            
        Returns:
            str: Validated category name
            
        Raises:
            ValidationError: If category is empty
        """
        if value is None or (isinstance(value, str) and not value.strip()):
            raise ValidationError(f"{field_name} is required and cannot be empty")
        
        return str(value).strip()
    
    @staticmethod
    def validate_optional_string(value: Any, field_name: str, max_length: Optional[int] = None) -> Optional[str]:
        """
        Validate optional string field.
        
        Args:
            value: String value to validate
            field_name: Name of the field for error messages
            max_length: Maximum allowed length
            
        Returns:
            Optional[str]: Validated string or None
            
        Raises:
            ValidationError: If string exceeds max length
        """
        if value is None or (isinstance(value, str) and not value.strip()):
            return None
        
        value_str = str(value).strip()
        
        if max_length and len(value_str) > max_length:
            raise ValidationError(f"{field_name} exceeds maximum length of {max_length}")
        
        return value_str
    
    @staticmethod
    def validate_boolean(value: Any, field_name: str, default: bool = True) -> bool:
        """
        Validate boolean field.
        
        Args:
            value: Boolean value to validate
            field_name: Name of the field for error messages
            default: Default value if None
            
        Returns:
            bool: Validated boolean value
        """
        if value is None:
            return default
        
        if isinstance(value, bool):
            return value
        
        if isinstance(value, str):
            value_lower = value.lower().strip()
            if value_lower in ('true', '1', 'yes', 'y'):
                return True
            elif value_lower in ('false', '0', 'no', 'n'):
                return False
        
        if isinstance(value, (int, float)):
            return bool(value)
        
        raise ValidationError(f"{field_name} must be a boolean value, got '{value}'")
    
    @staticmethod
    def validate_import_mode(mode: str) -> str:
        """
        Validate import mode.
        
        Args:
            mode: Import mode to validate
            
        Returns:
            str: Validated import mode
            
        Raises:
            ValidationError: If mode is invalid
        """
        if mode not in DataValidator.VALID_IMPORT_MODES:
            raise ValidationError(
                f"Import mode must be one of {DataValidator.VALID_IMPORT_MODES}, got '{mode}'"
            )
        return mode
    
    @staticmethod
    def validate_tags(value: Any) -> list[str]:
        """
        Validate and parse tags field.
        
        Args:
            value: Tags value (can be string with commas or list)
            
        Returns:
            list[str]: List of tag names
        """
        if value is None or (isinstance(value, str) and not value.strip()):
            return []
        
        if isinstance(value, list):
            return [str(tag).strip() for tag in value if str(tag).strip()]
        
        if isinstance(value, str):
            # Split by comma and clean up
            tags = [tag.strip() for tag in value.split(',') if tag.strip()]
            return tags
        
        return []


class DuplicateDetector:
    """Detector for duplicate transactions."""
    
    @staticmethod
    def generate_duplicate_key(
        transaction_date: date,
        amount: Decimal,
        description: Optional[str] = None
    ) -> str:
        """
        Generate a key for duplicate detection.
        
        Args:
            transaction_date: Transaction date
            amount: Transaction amount
            description: Optional transaction description
            
        Returns:
            str: Duplicate detection key
        """
        key_parts = [
            transaction_date.isoformat(),
            str(amount),
        ]
        
        if description:
            # Normalize description for comparison
            normalized_desc = description.lower().strip()
            key_parts.append(normalized_desc)
        
        return '|'.join(key_parts)
    
    @staticmethod
    def is_duplicate(
        key: str,
        existing_keys: set[str]
    ) -> bool:
        """
        Check if a transaction is a duplicate.
        
        Args:
            key: Duplicate detection key
            existing_keys: Set of existing keys
            
        Returns:
            bool: True if duplicate, False otherwise
        """
        return key in existing_keys

