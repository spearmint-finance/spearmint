#!/usr/bin/env python3
"""
Ensure an OpenAPI spec exists in Postman's Spec Hub.

This script uses a "find or create" strategy:
1. Search the workspace for a spec with the given name
2. If found, use that spec (self-healing - no hardcoded ID needed)
3. If not found, create a new spec

This approach makes the workflow self-healing - if a spec is deleted or
the hardcoded ID becomes stale, the workflow will find or recreate it.

Usage:
    # Find or create by name (recommended - self-healing)
    python ensure_spec.py \
        --workspace-id WORKSPACE_ID \
        --spec-file sdk/openapi.json \
        --spec-name "Spearmint Core API"

    # Check specific ID first, fall back to find-by-name
    python ensure_spec.py \
        --spec-id SPEC_ID \
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


def get_workspace_specs(workspace_id: str) -> list:
    """
    Get all specs in a workspace with their details.

    Args:
        workspace_id: ID of the workspace

    Returns:
        List of spec dictionaries with id, name, type, etc.
    """
    try:
        response = make_request(method='GET', path=f"/specs?workspaceId={workspace_id}")
        return response.get('specs', [])
    except Exception as e:
        print(f"  Warning: Could not list workspace specs: {e}")
        return []


def find_spec_by_name(workspace_id: str, spec_name: str) -> dict | None:
    """
    Find a spec in the workspace by name.

    Args:
        workspace_id: ID of the workspace
        spec_name: Name of the spec to find

    Returns:
        Spec info dictionary if found, None otherwise
    """
    specs = get_workspace_specs(workspace_id)
    for spec in specs:
        if spec.get('name') == spec_name:
            return spec
    return None


def check_spec_exists(spec_id: str) -> dict | None:
    """
    Check if a spec exists and is accessible in Postman.

    Args:
        spec_id: ID of the spec to check

    Returns:
        Spec info dictionary if it exists, None if not found (404) or
        inaccessible (403)
    """
    try:
        return make_request(method='GET', path=f"/specs/{spec_id}")
    except Exception as e:
        if "HTTP 404" in str(e) or "HTTP 403" in str(e):
            return None
        raise


def detect_spec_type(spec_content: str) -> str:
    """
    Detect the OpenAPI spec type from its content.

    The Postman API accepts: OPENAPI:3.0, ASYNCAPI:2.0

    Args:
        spec_content: Raw spec content string

    Returns:
        Spec type string for Postman API (e.g., "OPENAPI:3.0")
    """
    # Postman API only accepts OPENAPI:3.0 for all OpenAPI 3.x specs
    return "OPENAPI:3.0"


def update_spec_name(spec_id: str, name: str) -> dict:
    """
    Update the name of an existing spec.

    Args:
        spec_id: ID of the spec to update
        name: New name for the spec

    Returns:
        API response dictionary
    """
    return make_request(
        method='PATCH',
        path=f"/specs/{spec_id}",
        data={"name": name}
    )


def create_spec(workspace_id: str, spec_name: str, spec_content: str, spec_type: str) -> dict:
    """
    Create a new spec in Postman's Spec Hub.

    Args:
        workspace_id: Workspace ID to create the spec in
        spec_name: Name for the new spec
        spec_content: OpenAPI spec content string
        spec_type: Spec type (e.g., "openapi:3")

    Returns:
        API response dictionary with the created spec info
    """
    response = make_request(
        method='POST',
        path=f"/specs?workspaceId={workspace_id}",
        data={
            "name": spec_name,
            "type": spec_type,
            "files": [
                {
                    "path": "openapi.json",
                    "content": spec_content,
                    "type": "ROOT"
                }
            ]
        }
    )

    return response


def main():
    parser = argparse.ArgumentParser(
        description="Ensure an OpenAPI spec exists in Postman's Spec Hub"
    )
    parser.add_argument(
        '--spec-id',
        default='',
        help='ID of an existing spec to check first (optional, falls back to find-by-name)'
    )
    parser.add_argument(
        '--workspace-id',
        required=True,
        help='Workspace ID to find/create the spec in'
    )
    parser.add_argument(
        '--spec-file',
        required=True,
        help='Path to the OpenAPI spec file'
    )
    parser.add_argument(
        '--spec-name',
        default='Spearmint Core API',
        help='Name for the spec (used for find-by-name and creation)'
    )

    args = parser.parse_args()

    # Ensure API key is available
    get_api_key()

    print("Ensuring OpenAPI spec exists in Postman Spec Hub...")
    print(f"  Workspace ID: {args.workspace_id}")
    print(f"  Spec name: {args.spec_name}")
    print(f"  Spec file: {args.spec_file}")
    if args.spec_id:
        print(f"  Spec ID hint: {args.spec_id}")
    print()

    try:
        # Strategy 1: Check if the provided spec ID exists and is accessible
        if args.spec_id:
            print(f"Step 1: Checking if spec ID {args.spec_id} exists...")
            spec_info = check_spec_exists(args.spec_id)

            if spec_info is not None:
                print(f"  Found spec: {spec_info.get('name', 'N/A')}")

                # Update name if needed
                current_name = spec_info.get('name', '')
                if current_name != args.spec_name:
                    print(f"  Updating name: {current_name} -> {args.spec_name}")
                    try:
                        update_spec_name(args.spec_id, args.spec_name)
                    except Exception as e:
                        print(f"  Warning: Could not update name: {e}")

                print()
                print(f"Using existing spec (ID: {args.spec_id})")
                set_github_output("spec_id", args.spec_id)
                set_github_output("spec_created", "false")
                return 0
            else:
                print(f"  Spec ID not found or inaccessible.")
        else:
            print("Step 1: No spec ID provided, skipping ID check.")

        # Strategy 2: Find spec by name in the workspace
        print()
        print(f"Step 2: Searching workspace for spec named '{args.spec_name}'...")
        existing_spec = find_spec_by_name(args.workspace_id, args.spec_name)

        if existing_spec:
            found_id = existing_spec.get('id', '')
            print(f"  Found existing spec: {found_id}")
            print()
            print(f"Using existing spec (found by name)")
            print(f"  ID: {found_id}")
            print(f"  Name: {existing_spec.get('name', 'N/A')}")

            set_github_output("spec_id", found_id)
            set_github_output("spec_created", "false")
            return 0

        print(f"  No spec found with name '{args.spec_name}'")

        # Strategy 3: Create a new spec
        print()
        print("Step 3: Creating new spec...")

        # Read the spec file
        print("  Reading spec file...")
        spec_content = read_spec_file(args.spec_file)

        # Detect spec type
        spec_type = detect_spec_type(spec_content)
        print(f"  Detected spec type: {spec_type}")

        # Create the spec
        print(f"  Creating spec: {args.spec_name}...")
        response = create_spec(args.workspace_id, args.spec_name, spec_content, spec_type)

        new_spec_id = response.get('id', '')
        if not new_spec_id:
            # Try alternate response structures
            new_spec_id = response.get('spec', {}).get('id', '')

        if not new_spec_id:
            raise Exception(f"Could not extract spec ID from response: {response}")

        print()
        print("Spec created successfully!")
        print(f"  ID: {new_spec_id}")
        print(f"  Name: {args.spec_name}")

        set_github_output("spec_id", new_spec_id)
        set_github_output("spec_created", "true")
        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main())
