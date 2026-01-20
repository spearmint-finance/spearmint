#!/usr/bin/env python3
"""
Update a Postman collection's description with version changelog.

This script updates the collection description to include version info
and links to historical forks.

Usage:
    python update_collection_description.py \
        --collection-id COLLECTION_ID \
        --version 1.0.0

Environment:
    POSTMAN_API_KEY: Postman API key (required)
"""

import argparse
import os
import sys
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from postman.common import get_api_key, make_request, set_github_output


def get_collection(collection_id: str) -> dict:
    """
    Get collection details.
    
    Args:
        collection_id: ID of the collection
        
    Returns:
        Collection data dictionary
    """
    return make_request(method='GET', path=f"/collections/{collection_id}")


def patch_collection(collection_id: str, updates: dict) -> dict:
    """
    Patch a collection with updates.
    
    Args:
        collection_id: ID of the collection
        updates: Dictionary of updates to apply
        
    Returns:
        API response
    """
    return make_request(
        method='PATCH',
        path=f"/collections/{collection_id}",
        data={"collection": updates}
    )


def get_collection_forks(collection_id: str) -> list:
    """
    Get list of collection forks.
    
    Args:
        collection_id: ID of the collection
        
    Returns:
        List of fork information
    """
    response = make_request(method='GET', path=f"/collections/{collection_id}/forks")
    return response.get('forks', [])


def build_description(version: str, forks: list, base_description: str = "") -> str:
    """
    Build the collection description with version info and fork links.
    
    Args:
        version: Current version
        forks: List of fork information
        base_description: Base description to preserve
        
    Returns:
        Updated description string
    """
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Start with base description (strip any existing version section)
    desc_parts = base_description.split("---\n## Version History")
    base = desc_parts[0].strip()
    
    lines = []
    if base:
        lines.append(base)
        lines.append("")
    
    lines.append("---")
    lines.append("## Version History")
    lines.append("")
    lines.append(f"**Current Version:** v{version} (updated {current_date})")
    lines.append("")
    
    if forks:
        lines.append("### Previous Versions (Forks)")
        lines.append("")
        for fork in forks[:10]:  # Limit to 10 most recent
            label = fork.get('label', 'Unknown version')
            created = fork.get('createdAt', 'Unknown date')[:10]
            lines.append(f"- **{label}** - {created}")
        lines.append("")
    
    lines.append("*Spec version history available via Git tags.*")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Update a Postman collection's description with version changelog"
    )
    parser.add_argument(
        '--collection-id',
        required=True,
        help='ID of the collection to update'
    )
    parser.add_argument(
        '--version',
        required=True,
        help='Current API version'
    )
    parser.add_argument(
        '--base-description',
        help='Base description to preserve (default: read from collection)'
    )
    
    args = parser.parse_args()
    
    # Ensure API key is available
    get_api_key()
    
    print(f"Updating collection description...")
    print(f"  Collection ID: {args.collection_id}")
    print(f"  Version: {args.version}")
    print()
    
    try:
        # Get current collection info
        print("Getting current collection info...")
        collection_data = get_collection(args.collection_id)
        collection = collection_data.get('collection', {})
        info = collection.get('info', {})
        current_desc = args.base_description or info.get('description', '')
        
        # Get forks for version history
        print("Getting collection forks...")
        forks = get_collection_forks(args.collection_id)
        print(f"  Found {len(forks)} forks")
        
        # Build new description
        new_description = build_description(args.version, forks, current_desc)
        
        # Update the collection
        print()
        print("Updating collection description...")
        # Note: PATCH endpoint only accepts 'name' and 'description' in info
        # Do NOT include 'schema' - it causes a 400 error
        patch_collection(args.collection_id, {
            "info": {
                "name": info.get('name'),
                "description": new_description
            }
        })
        
        print()
        print("✓ Collection description updated successfully!")
        
        # Set GitHub outputs
        set_github_output("description_updated", "true")
        
        return 0
        
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main())

