#!/usr/bin/env python3
"""
Ensure an OpenAPI spec exists in Postman's Spec Hub.

Checks if the spec exists (by ID). If it doesn't exist or the ID is empty,
creates a new spec in the specified workspace. This enables bootstrap/first-run
support for the CI/CD workflow.

Usage:
    python ensure_spec.py \
        --spec-id SPEC_ID \
        --workspace-id WORKSPACE_ID \
        --spec-file sdk/openapi.json

    # First run (no existing spec):
    python ensure_spec.py \
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

    Args:
        spec_content: Raw spec content string

    Returns:
        Spec type string (e.g., "openapi:3_1" or "openapi:3")
    """
    try:
        spec_data = json.loads(spec_content)
    except json.JSONDecodeError:
        return "openapi:3"

    openapi_version = spec_data.get("openapi", "")
    if openapi_version.startswith("3.1"):
        return "openapi:3_1"
    return "openapi:3"


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
        help='ID of the existing spec to check (optional, empty means create new)'
    )
    parser.add_argument(
        '--workspace-id',
        required=True,
        help='Workspace ID to create the spec in (if needed)'
    )
    parser.add_argument(
        '--spec-file',
        required=True,
        help='Path to the OpenAPI spec file'
    )
    parser.add_argument(
        '--spec-name',
        default='Spearmint Core API',
        help='Name for the spec (default: "Spearmint Core API")'
    )

    args = parser.parse_args()

    # Ensure API key is available
    get_api_key()

    print("Ensuring OpenAPI spec exists in Postman Spec Hub...")
    print(f"  Spec ID: {args.spec_id or '(not provided)'}")
    print(f"  Workspace ID: {args.workspace_id}")
    print(f"  Spec file: {args.spec_file}")
    print()

    try:
        # Check if spec already exists
        if args.spec_id:
            print(f"Checking if spec {args.spec_id} exists...")
            spec_info = check_spec_exists(args.spec_id)

            if spec_info is not None:
                print(f"  Spec exists: {spec_info.get('name', 'N/A')}")
                print()
                print("Spec already exists, no action needed.")

                set_github_output("spec_id", args.spec_id)
                set_github_output("spec_created", "false")
                return 0

            print(f"  Spec not found or inaccessible. Will create a new one.")
            print()

        # Read the spec file
        print("Reading spec file...")
        spec_content = read_spec_file(args.spec_file)

        # Detect spec type
        spec_type = detect_spec_type(spec_content)
        print(f"  Detected spec type: {spec_type}")

        # Create the spec
        print(f"Creating new spec: {args.spec_name}...")
        response = create_spec(args.workspace_id, args.spec_name, spec_content, spec_type)

        new_spec_id = response.get('id', '')
        if not new_spec_id:
            # Try alternate response structures
            new_spec_id = response.get('spec', {}).get('id', '')

        if not new_spec_id:
            print("ERROR: Could not extract spec ID from creation response", file=sys.stderr)
            print(f"  Response: {response}", file=sys.stderr)
            sys.exit(1)

        print()
        print("Spec created successfully!")
        print(f"  New Spec ID: {new_spec_id}")
        print(f"  Name: {args.spec_name}")

        set_github_output("spec_id", new_spec_id)
        set_github_output("spec_created", "true")

        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main())
