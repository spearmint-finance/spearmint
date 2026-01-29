#!/usr/bin/env python3
"""
Ensure a Postman collection exists for the API.

This script uses a "find or create" strategy:
1. Check if the provided collection ID exists (optional hint)
2. Search the workspace for a collection with the given name
3. If found, use that collection (self-healing - no hardcoded ID needed)
4. If not found, import the OpenAPI spec as a new collection

This approach makes the workflow self-healing - if a collection is deleted or
the hardcoded ID becomes stale, the workflow will find or recreate it.

Usage:
    # Find or create by name (recommended - self-healing)
    python ensure_collection.py \
        --workspace-id WORKSPACE_ID \
        --spec-file sdk/openapi.json \
        --collection-name "Spearmint Core API"

    # Check specific ID first, fall back to find-by-name
    python ensure_collection.py \
        --collection-id COLLECTION_UID \
        --workspace-id WORKSPACE_ID \
        --spec-file sdk/openapi.json

Environment:
    POSTMAN_API_KEY: Postman API key (required)
"""

import argparse
import json
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from postman.common import get_api_key, make_request, read_spec_file, set_github_output


def get_workspace_collections(workspace_id: str) -> list:
    """
    Get all collections in a workspace with their details.

    Args:
        workspace_id: ID of the workspace

    Returns:
        List of collection dictionaries with id, uid, name, etc.
    """
    try:
        response = make_request(method='GET', path=f"/workspaces/{workspace_id}")
        workspace = response.get('workspace', {})
        return workspace.get('collections', [])
    except Exception as e:
        print(f"  Warning: Could not list workspace collections: {e}")
        return []


def find_collection_by_name(workspace_id: str, collection_name: str) -> dict | None:
    """
    Find a collection in the workspace by name.

    Args:
        workspace_id: ID of the workspace
        collection_name: Name of the collection to find

    Returns:
        Collection info dictionary if found, None otherwise
    """
    collections = get_workspace_collections(workspace_id)
    for collection in collections:
        if collection.get('name') == collection_name:
            return collection
    return None


def check_collection_exists(collection_id: str) -> dict | None:
    """
    Check if a collection exists and is accessible in Postman.

    Args:
        collection_id: UID of the collection to check

    Returns:
        Collection info dictionary if it exists, None if not found (404) or
        inaccessible (403)
    """
    try:
        return make_request(method='GET', path=f"/collections/{collection_id}")
    except Exception as e:
        if "HTTP 404" in str(e) or "HTTP 403" in str(e):
            return None
        raise


def update_collection_name(collection_id: str, name: str) -> dict:
    """
    Update the name of an existing collection.

    Args:
        collection_id: UID of the collection to update
        name: New name for the collection

    Returns:
        API response dictionary
    """
    return make_request(
        method='PATCH',
        path=f"/collections/{collection_id}",
        data={"collection": {"info": {"name": name}}}
    )


def create_collection_from_spec(workspace_id: str, spec_content: str, collection_name: str) -> dict:
    """
    Create a new collection by importing an OpenAPI spec.

    Injects the collection name into the spec's info.title field before import
    so the resulting collection has the desired name.

    Args:
        workspace_id: Workspace ID to create the collection in
        spec_content: OpenAPI spec content string
        collection_name: Desired name for the collection

    Returns:
        API response dictionary with the created collection info
    """
    # Set the spec title to the desired collection name
    try:
        spec_data = json.loads(spec_content)
        spec_data.setdefault('info', {})['title'] = collection_name
        modified_spec = json.dumps(spec_data)
    except (json.JSONDecodeError, TypeError):
        modified_spec = spec_content

    response = make_request(
        method='POST',
        path=f"/import/openapi?workspace={workspace_id}",
        data={
            "type": "string",
            "input": modified_spec,
            "options": {
                "folderStrategy": "Tags",
                "requestParametersResolution": "Schema",
                "exampleParametersResolution": "Schema"
            }
        }
    )

    return response


def main():
    parser = argparse.ArgumentParser(
        description="Ensure a Postman collection exists for the API"
    )
    parser.add_argument(
        '--collection-id',
        default='',
        help='UID of an existing collection to check first (optional, falls back to find-by-name)'
    )
    parser.add_argument(
        '--workspace-id',
        required=True,
        help='Workspace ID to find/create the collection in'
    )
    parser.add_argument(
        '--spec-file',
        required=True,
        help='Path to the OpenAPI spec file (used for import if creating)'
    )
    parser.add_argument(
        '--collection-name',
        default='Spearmint Core API',
        help='Name for the collection (used for find-by-name and creation)'
    )

    args = parser.parse_args()

    # Ensure API key is available
    get_api_key()

    print("Ensuring Postman collection exists...")
    print(f"  Workspace ID: {args.workspace_id}")
    print(f"  Collection name: {args.collection_name}")
    print(f"  Spec file: {args.spec_file}")
    if args.collection_id:
        print(f"  Collection ID hint: {args.collection_id}")
    print()

    try:
        # Strategy 1: Check if the provided collection ID exists and is accessible
        if args.collection_id:
            print(f"Step 1: Checking if collection ID {args.collection_id} exists...")
            collection_info = check_collection_exists(args.collection_id)

            if collection_info is not None:
                collection = collection_info.get('collection', {})
                current_name = collection.get('info', {}).get('name', '')
                print(f"  Found collection: {current_name}")

                # Update name if needed
                if current_name != args.collection_name:
                    print(f"  Updating name: {current_name} -> {args.collection_name}")
                    try:
                        update_collection_name(args.collection_id, args.collection_name)
                    except Exception as e:
                        print(f"  Warning: Could not update name: {e}")

                print()
                print(f"Using existing collection (ID: {args.collection_id})")
                set_github_output("collection_uid", args.collection_id)
                set_github_output("collection_created", "false")
                return 0
            else:
                print(f"  Collection ID not found or inaccessible.")
        else:
            print("Step 1: No collection ID provided, skipping ID check.")

        # Strategy 2: Find collection by name in the workspace
        print()
        print(f"Step 2: Searching workspace for collection named '{args.collection_name}'...")
        existing_collection = find_collection_by_name(args.workspace_id, args.collection_name)

        if existing_collection:
            found_uid = existing_collection.get('uid', '')
            print(f"  Found existing collection: {found_uid}")
            print()
            print(f"Using existing collection (found by name)")
            print(f"  UID: {found_uid}")
            print(f"  Name: {existing_collection.get('name', 'N/A')}")

            set_github_output("collection_uid", found_uid)
            set_github_output("collection_created", "false")
            return 0

        print(f"  No collection found with name '{args.collection_name}'")

        # Strategy 3: Create a new collection from OpenAPI spec
        print()
        print("Step 3: Creating new collection from OpenAPI spec...")

        # Read the spec file
        print("  Reading spec file...")
        spec_content = read_spec_file(args.spec_file)

        # Create collection via OpenAPI import
        print(f"  Importing spec as collection: {args.collection_name}...")
        response = create_collection_from_spec(
            args.workspace_id, spec_content, args.collection_name
        )

        # Extract collection UID from response
        # The import/openapi endpoint returns {"collections": [{"id": "...", "uid": "..."}]}
        collections = response.get('collections', [])
        if collections:
            new_uid = collections[0].get('uid', '')
            new_id = collections[0].get('id', '')
        else:
            new_uid = ''
            new_id = ''

        if not new_uid:
            raise Exception(f"Could not extract collection UID from response: {response}")

        print()
        print("Collection created successfully!")
        print(f"  UID: {new_uid}")
        print(f"  ID: {new_id}")
        print(f"  Name: {args.collection_name}")

        set_github_output("collection_uid", new_uid)
        set_github_output("collection_created", "true")
        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main())
