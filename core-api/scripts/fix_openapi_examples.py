#!/usr/bin/env python3
"""
Fix OpenAPI spec examples to match schema property types.
Also fixes schema naming issues to comply with PascalCase.

This script is schema-aware: it reads the actual property type definitions
from components.schemas and ensures examples match those types exactly.
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional


def get_schema_type(spec: Dict, schema_ref: str) -> Optional[str]:
    """Extract the actual type from a schema reference."""
    if not schema_ref.startswith('#/components/schemas/'):
        return None
    
    schema_name = schema_ref.replace('#/components/schemas/', '')
    schemas = spec.get('components', {}).get('schemas', {})
    
    return schemas.get(schema_name)


def get_property_type(schema: Dict, property_name: str) -> Optional[str]:
    """
    Determine the expected type for a property from its schema definition.
    Returns: 'string', 'integer', 'number', 'boolean', 'object', 'array', or None
    """
    if not schema or 'properties' not in schema:
        return None
    
    prop_def = schema['properties'].get(property_name)
    if not prop_def:
        return None
    
    # Handle anyOf/oneOf (nullable types)
    if 'anyOf' in prop_def:
        for option in prop_def['anyOf']:
            if option.get('type') and option['type'] != 'null':
                return option['type']
    
    if 'oneOf' in prop_def:
        for option in prop_def['oneOf']:
            if option.get('type') and option['type'] != 'null':
                return option['type']
    
    # Direct type
    return prop_def.get('type')


def fix_example_value(value: Any, expected_type: str) -> Any:
    """Convert a value to match the expected schema type."""
    if value is None:
        return value
    
    if expected_type == 'string':
        if isinstance(value, bool):
            return str(value).lower()  # true -> "true"
        elif isinstance(value, (int, float)):
            # Format numbers as decimal strings
            if isinstance(value, float) or '.' in str(value):
                return f"{float(value):.2f}"
            else:
                return str(value)
        else:
            return str(value)
    
    elif expected_type == 'integer':
        if isinstance(value, str):
            try:
                return int(float(value))
            except (ValueError, TypeError):
                return value
        elif isinstance(value, bool):
            return int(value)
        elif isinstance(value, float):
            return int(value)
        else:
            return value
    
    elif expected_type == 'number':
        if isinstance(value, str):
            try:
                return float(value)
            except (ValueError, TypeError):
                return value
        elif isinstance(value, bool):
            return float(value)
        else:
            return value
    
    elif expected_type == 'boolean':
        if isinstance(value, str):
            return value.lower() in ('true', '1', 'yes')
        else:
            return bool(value)
    
    # For object and array, return as-is (recursion happens elsewhere)
    return value


def fix_schema_examples(spec: Dict):
    """
    Fix all examples in schema definitions to match property types.
    Also converts Decimal fields (number type) to string type in the schema.
    """
    schemas = spec.get('components', {}).get('schemas', {})
    
    for schema_name, schema in schemas.items():
        if not isinstance(schema, dict):
            continue
        
        # Convert number types to string for monetary/decimal fields
        # This aligns with Pydantic's json_encoders={Decimal: str}
        if 'properties' in schema:
            for prop_name, prop_def in schema['properties'].items():
                # Convert number to string for decimal-like fields
                if prop_def.get('type') == 'number' and _is_decimal_field(prop_name):
                    prop_def['type'] = 'string'
                    prop_def['format'] = 'decimal'
                
                # Handle anyOf for Optional fields
                if 'anyOf' in prop_def:
                    for option in prop_def['anyOf']:
                        if option.get('type') == 'number' and _is_decimal_field(prop_name):
                            option['type'] = 'string'
                            option['format'] = 'decimal'
        
        # Fix examples in the schema itself
        if 'example' in schema and isinstance(schema['example'], dict):
            schema['example'] = fix_example_object(spec, schema, schema['example'])
        
        # Fix examples in properties
        if 'properties' in schema:
            for prop_name, prop_def in schema['properties'].items():
                if 'example' in prop_def:
                    expected_type = get_property_type(schema, prop_name)
                    if expected_type:
                        prop_def['example'] = fix_example_value(prop_def['example'], expected_type)


def _is_decimal_field(field_name: str) -> bool:
    """Determine if a field name suggests it's a Decimal/monetary field."""
    field_lower = field_name.lower()
    
    # Exclude non-monetary fields first
    exclude_patterns = [
        '_count', 'count', '_id', 'id', 'exclude_', 'is_', 'has_',
        '_calc', 'calc_', '_flag', 'flag_', 'created_', 'updated_'
    ]
    if any(pattern in field_lower for pattern in exclude_patterns):
        return False
    
    # Include fields that are likely decimal/monetary
    decimal_keywords = [
        'amount', 'total', 'balance', 'value', 'income', 'expense',
        'cash_flow', 'net_', 'average_', 'daily_', 'price', 'cost',
        'revenue', 'profit', 'loss', 'payment', 'deposit', 'withdrawal'
    ]
    
    return any(keyword in field_lower for keyword in decimal_keywords)


def fix_example_object(spec: Dict, schema: Dict, example: Any) -> Any:
    """Fix an example object to match schema property types."""
    if not isinstance(example, dict):
        return example
    
    if not schema or 'properties' not in schema:
        return example
    
    fixed_example = {}
    
    for key, value in example.items():
        expected_type = get_property_type(schema, key)
        
        if expected_type in ('object', 'array'):
            # Recursively handle nested objects/arrays
            if isinstance(value, dict):
                # Try to find nested schema for object reference
                prop_def = schema['properties'].get(key, {})
                if '$ref' in prop_def:
                    nested_schema_name = prop_def['$ref'].replace('#/components/schemas/', '')
                    nested_schema = spec.get('components', {}).get('schemas', {}).get(nested_schema_name)
                    if nested_schema:
                        fixed_example[key] = fix_example_object(spec, nested_schema, value)
                    else:
                        fixed_example[key] = value
                else:
                    fixed_example[key] = value
            elif isinstance(value, list):
                # Handle arrays - need to find item schema
                prop_def = schema['properties'].get(key, {})
                item_schema = None
                
                # Check if array has items with $ref
                if 'items' in prop_def and '$ref' in prop_def['items']:
                    item_schema_name = prop_def['items']['$ref'].replace('#/components/schemas/', '')
                    item_schema = spec.get('components', {}).get('schemas', {}).get(item_schema_name)
                
                if item_schema:
                    fixed_example[key] = [
                        fix_example_object(spec, item_schema, item) if isinstance(item, dict) else item
                        for item in value
                    ]
                else:
                    fixed_example[key] = value
            else:
                fixed_example[key] = value
        elif expected_type:
            fixed_example[key] = fix_example_value(value, expected_type)
        else:
            # No type found, keep as-is
            fixed_example[key] = value
    
    return fixed_example


def fix_schema_names(spec):
    """Fix schema naming issues to comply with PascalCase rule."""
    if 'components' not in spec or 'schemas' not in spec['components']:
        return
    
    schemas = spec['components']['schemas']
    renames = {}
    
    # Find schemas that need renaming
    for schema_name in list(schemas.keys()):
        new_name = schema_name
        
        # Fix hyphenated names
        if '-' in schema_name:
            new_name = schema_name.replace('-', '')
        
        # Fix underscore names (convert to PascalCase)
        if '_' in schema_name:
            parts = schema_name.split('_')
            new_name = ''.join(word.capitalize() for word in parts)
        
        # Fix double-underscore paths (FastAPI internal naming)
        if '__' in schema_name:
            parts = schema_name.split('__')
            # Take last meaningful part and capitalize
            new_name = ''.join(word.capitalize() for word in parts[-1].split('_'))
            # Add suffix to avoid collisions
            if new_name in schemas and new_name != schema_name:
                # Use module path hint
                if 'analysis' in schema_name.lower():
                    new_name = new_name + 'Analysis'
                elif 'report' in schema_name.lower():
                    new_name = new_name + 'Report'
        
        if new_name != schema_name:
            renames[schema_name] = new_name
    
    # Apply renames
    for old_name, new_name in renames.items():
        # Rename in schemas dict
        schemas[new_name] = schemas.pop(old_name)
        
        # Update all $ref references
        update_refs(spec, old_name, new_name)


def update_refs(obj, old_name, new_name):
    """Recursively update $ref references."""
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == '$ref' and isinstance(value, str):
                if value == f"#/components/schemas/{old_name}":
                    obj[key] = f"#/components/schemas/{new_name}"
            else:
                update_refs(value, old_name, new_name)
    elif isinstance(obj, list):
        for item in obj:
            update_refs(item, old_name, new_name)


def main():
    if len(sys.argv) < 2:
        print("Usage: python fix_openapi_examples.py <openapi.json>")
        sys.exit(1)
    
    spec_path = Path(sys.argv[1])
    
    if not spec_path.exists():
        print(f"Error: {spec_path} not found")
        sys.exit(1)
    
    print(f"Loading spec: {spec_path}")
    with open(spec_path, 'r', encoding='utf-8') as f:
        spec = json.load(f)
    
    print("Fixing schema examples to match property types...")
    fix_schema_examples(spec)
    
    print("Fixing schema names...")
    fix_schema_names(spec)
    
    print(f"Writing fixed spec: {spec_path}")
    with open(spec_path, 'w', encoding='utf-8') as f:
        json.dump(spec, f, indent=2)
    
    print("✓ OpenAPI spec fixed successfully")


if __name__ == '__main__':
    main()
