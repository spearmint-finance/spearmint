#!/usr/bin/env python3
# Fork collection script for Postman versioning
"""
Fork a Postman collection to create a version snapshot.

This script creates a fork of the current collection before updating it,
preserving the previous version as a labeled snapshot.

Usage:
    python fork_collection.py \
        --collection-id COLLECTION_ID \
        --workspace-id WORKSPACE_ID \
        --version 1.0.0

Environment:
    POSTMAN_API_KEY: Postman API key (required)
"""

import argparse
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from postman.common import get_api_key, make_request, set_github_output


def fork_collection(collection_id: str, workspace_id: str, label: str) -> dict:
    """
    Create a fork of a collection.
    
    Args:
        collection_id: ID of the collection to fork
        workspace_id: Workspace ID to create the fork in
        label: Label for the fork (e.g., "v1.0.0 snapshot")
        
    Returns:
        API response with fork information
    """
    response = make_request(
        method='POST',
        path=f"/collections/fork/{collection_id}?workspace={workspace_id}",
        data={"label": label}
    )
    
    return response


def get_collection_info(collection_id: str) -> dict:
    """
    Get information about a collection.
    
    Args:
        collection_id: ID of the collection
        
    Returns:
        Collection information dictionary
    """
    return make_request(method='GET', path=f"/collections/{collection_id}")


def list_collection_forks(collection_id: str) -> dict:
    """
    List all forks of a collection.
    
    Args:
        collection_id: ID of the collection
        
    Returns:
        List of forks
    """
    return make_request(method='GET', path=f"/collections/{collection_id}/forks")


def main():
    parser = argparse.ArgumentParser(
        description="Fork a Postman collection to create a version snapshot"
    )
    parser.add_argument(
        '--collection-id',
        required=True,
        help='ID of the collection to fork'
    )
    parser.add_argument(
        '--workspace-id',
        required=True,
        help='Workspace ID to create the fork in'
    )
    parser.add_argument(
        '--version',
        required=True,
        help='Version label for the fork (e.g., 1.0.0)'
    )
    parser.add_argument(
        '--label-format',
        default='v{version} snapshot',
        help='Format for fork label (default: "v{version} snapshot")'
    )
    
    args = parser.parse_args()
    
    # Ensure API key is available
    get_api_key()
    
    # Create the fork label
    fork_label = args.label_format.format(version=args.version)
    
    print(f"Creating collection fork (version snapshot)...")
    print(f"  Collection ID: {args.collection_id}")
    print(f"  Workspace ID: {args.workspace_id}")
    print(f"  Fork label: {fork_label}")
    print()
    
    try:
        # Get current collection info
        print("Getting current collection info...")
        collection_info = get_collection_info(args.collection_id)
        collection_name = collection_info.get('collection', {}).get('info', {}).get('name', 'Unknown')
        print(f"  Collection name: {collection_name}")
        print()
        
        # Create the fork
        print(f"Creating fork: {fork_label}...")
        response = fork_collection(args.collection_id, args.workspace_id, fork_label)
        
        fork_info = response.get('collection', response)
        fork_id = fork_info.get('id', 'N/A')
        fork_uid = fork_info.get('uid', 'N/A')
        
        print()
        print("✓ Fork created successfully!")
        print()
        print("Fork Details:")
        print(f"  Label: {fork_label}")
        print(f"  ID:    {fork_id}")
        print(f"  UID:   {fork_uid}")
        
        # Set GitHub outputs
        set_github_output("fork_id", fork_id)
        set_github_output("fork_uid", fork_uid)
        set_github_output("fork_label", fork_label)
        
        return 0
        
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main())

