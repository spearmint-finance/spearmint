#!/usr/bin/env python3
"""
Re-import a Postman collection from an OpenAPI spec.

Deletes the existing collection and creates a fresh one from the spec,
ensuring the collection always reflects the latest endpoints.

Usage:
    python reimport_collection.py \
        --collection-id COLLECTION_UID \
        --workspace-id WORKSPACE_ID \
        --spec-file sdk/openapi.json \
        --collection-name "Spearmint Core API"

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


def delete_collection(collection_uid: str):
    """Delete a collection by UID."""
    make_request(method='DELETE', path=f"/collections/{collection_uid}")


def create_collection_from_spec(workspace_id: str, spec_content: str, collection_name: str) -> dict:
    """Create a new collection by importing an OpenAPI spec."""
    try:
        spec_data = json.loads(spec_content)
        spec_data.setdefault('info', {})['title'] = collection_name
        modified_spec = json.dumps(spec_data)
    except (json.JSONDecodeError, TypeError):
        modified_spec = spec_content

    return make_request(
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


def main():
    parser = argparse.ArgumentParser(
        description="Re-import a Postman collection from an OpenAPI spec"
    )
    parser.add_argument('--collection-id', required=True, help='UID of the existing collection to replace')
    parser.add_argument('--workspace-id', required=True, help='Workspace ID')
    parser.add_argument('--spec-file', required=True, help='Path to the OpenAPI spec file')
    parser.add_argument('--collection-name', default='Spearmint Core API', help='Name for the collection')

    args = parser.parse_args()
    get_api_key()

    print("Re-importing Postman collection from spec...")
    print(f"  Collection ID: {args.collection_id}")
    print(f"  Workspace ID: {args.workspace_id}")
    print(f"  Spec file: {args.spec_file}")
    print(f"  Collection name: {args.collection_name}")
    print()

    try:
        # Step 1: Delete old collection
        print("Deleting old collection...")
        delete_collection(args.collection_id)
        print("  Done.")
        print()

        # Step 2: Import fresh collection from spec
        print("Importing new collection from spec...")
        spec_content = read_spec_file(args.spec_file)
        response = create_collection_from_spec(
            args.workspace_id, spec_content, args.collection_name
        )

        collections = response.get('collections', [])
        if not collections:
            raise Exception(f"No collection returned from import: {response}")

        new_uid = collections[0].get('uid', '')
        new_id = collections[0].get('id', '')

        print(f"  New UID: {new_uid}")
        print(f"  New ID: {new_id}")
        print()
        print("✓ Collection re-imported successfully!")

        set_github_output("collection_uid", new_uid)
        set_github_output("reimport_status", "success")

        # Warn if UID changed (workflow env var may need updating)
        if new_uid != args.collection_id:
            print()
            print(f"⚠️  Collection UID changed: {args.collection_id} -> {new_uid}")
            print("   Update POSTMAN_COLLECTION_UID in the workflow env vars.")

        return 0

    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main())
