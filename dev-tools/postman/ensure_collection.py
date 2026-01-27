#!/usr/bin/env python3
"""
Ensure a Postman collection exists for the API.

Checks if the collection exists (by ID). If it doesn't exist or the ID is empty,
imports the OpenAPI spec as a new collection in the specified workspace.
This enables bootstrap/first-run support for the CI/CD workflow.

Usage:
    python ensure_collection.py \
        --collection-id COLLECTION_UID \
        --workspace-id WORKSPACE_ID \
        --spec-file sdk/openapi.json

    # First run (no existing collection):
    python ensure_collection.py \
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


def check_collection_exists(collection_id: str) -> dict | None:
    """
    Check if a collection exists in Postman.

    Args:
        collection_id: UID of the collection to check

    Returns:
        Collection info dictionary if it exists, None if not found (404)
    """
    try:
        return make_request(method='GET', path=f"/collections/{collection_id}")
    except Exception as e:
        if "HTTP 404" in str(e):
            return None
        raise


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
        help='UID of the existing collection to check (optional, empty means create new)'
    )
    parser.add_argument(
        '--workspace-id',
        required=True,
        help='Workspace ID to create the collection in (if needed)'
    )
    parser.add_argument(
        '--spec-file',
        required=True,
        help='Path to the OpenAPI spec file (used for import if creating)'
    )
    parser.add_argument(
        '--collection-name',
        default='Spearmint Finance API',
        help='Name for the collection (default: "Spearmint Finance API")'
    )

    args = parser.parse_args()

    # Ensure API key is available
    get_api_key()

    print("Ensuring Postman collection exists...")
    print(f"  Collection ID: {args.collection_id or '(not provided)'}")
    print(f"  Workspace ID: {args.workspace_id}")
    print(f"  Spec file: {args.spec_file}")
    print()

    try:
        # Check if collection already exists
        if args.collection_id:
            print(f"Checking if collection {args.collection_id} exists...")
            collection_info = check_collection_exists(args.collection_id)

            if collection_info is not None:
                collection = collection_info.get('collection', {})
                name = collection.get('info', {}).get('name', 'N/A')
                print(f"  Collection exists: {name}")
                print()
                print("Collection already exists, no action needed.")

                set_github_output("collection_uid", args.collection_id)
                set_github_output("collection_created", "false")
                return 0

            print(f"  Collection not found (404). Will create a new one.")
            print()

        # Read the spec file for import
        print("Reading spec file...")
        spec_content = read_spec_file(args.spec_file)

        # Create collection via OpenAPI import
        print(f"Creating collection from OpenAPI spec: {args.collection_name}...")
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
            print("ERROR: Could not extract collection UID from import response", file=sys.stderr)
            print(f"  Response: {response}", file=sys.stderr)
            sys.exit(1)

        print()
        print("Collection created successfully!")
        print(f"  Collection UID: {new_uid}")
        print(f"  Collection ID: {new_id}")
        print(f"  Name: {args.collection_name}")

        set_github_output("collection_uid", new_uid)
        set_github_output("collection_created", "true")

        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main())
