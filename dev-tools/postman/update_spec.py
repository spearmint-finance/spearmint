#!/usr/bin/env python3
"""
Update an existing OpenAPI spec in Postman's Spec Hub.

This script updates the spec file content in-place rather than creating a new spec.
It's part of the versioning strategy that maintains a single "current" spec.

Usage:
    python update_spec.py \
        --spec-id SPEC_ID \
        --spec-file sdk/openapi.json \
        --version 1.0.0

Environment:
    POSTMAN_API_KEY: Postman API key (required)
"""

import argparse
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from postman.common import get_api_key, make_request, read_spec_file, set_github_output


def create_spec_file(spec_id: str, spec_content: str, file_path: str = "openapi.json") -> dict:
    """
    Create a new spec file in Postman Spec Hub.

    Args:
        spec_id: ID of the spec
        spec_content: Content for the spec file
        file_path: Path of the file within the spec (default: openapi.json)

    Returns:
        API response dictionary
    """
    response = make_request(
        method='POST',
        path=f"/specs/{spec_id}/files",
        data={"path": file_path, "content": spec_content}
    )

    return response


def update_spec_file(spec_id: str, spec_content: str, file_path: str = "openapi.json") -> dict:
    """
    Update the content of a spec file in Postman Spec Hub.

    Args:
        spec_id: ID of the spec to update
        spec_content: New content for the spec file
        file_path: Path of the file within the spec (default: openapi.json)

    Returns:
        API response dictionary
    """
    # URL-encode the file path for the API endpoint
    encoded_path = file_path.replace("/", "%2F")

    response = make_request(
        method='PUT',
        path=f"/specs/{spec_id}/files/{encoded_path}",
        data={"content": spec_content}
    )

    return response


def update_spec_properties(spec_id: str, name: str) -> dict:
    """
    Update spec properties like name.
    
    Args:
        spec_id: ID of the spec to update
        name: New name for the spec
        
    Returns:
        API response dictionary
    """
    response = make_request(
        method='PUT',
        path=f"/specs/{spec_id}",
        data={"name": name}
    )
    
    return response


def get_spec_info(spec_id: str) -> dict:
    """
    Get information about a spec.

    Args:
        spec_id: ID of the spec

    Returns:
        Spec information dictionary
    """
    return make_request(method='GET', path=f"/specs/{spec_id}")


def get_spec_files(spec_id: str) -> list:
    """
    Get list of files in a spec.

    Args:
        spec_id: ID of the spec

    Returns:
        List of file information dictionaries
    """
    response = make_request(method='GET', path=f"/specs/{spec_id}/files")
    return response.get('files', [])


def main():
    parser = argparse.ArgumentParser(
        description="Update an existing OpenAPI spec in Postman's Spec Hub"
    )
    parser.add_argument(
        '--spec-id',
        required=True,
        help='ID of the existing spec to update'
    )
    parser.add_argument(
        '--spec-file',
        required=True,
        help='Path to the OpenAPI spec file'
    )
    parser.add_argument(
        '--version',
        required=True,
        help='API version (e.g., 1.0.0)'
    )
    parser.add_argument(
        '--update-name',
        action='store_true',
        help='Also update the spec name to include version'
    )
    parser.add_argument(
        '--spec-name',
        help='Custom name for the spec (default: "Spearmint Finance API")'
    )
    
    args = parser.parse_args()
    
    # Ensure API key is available
    get_api_key()
    
    spec_name = args.spec_name or "Spearmint Finance API"
    
    print(f"Updating OpenAPI spec in Postman Spec Hub...")
    print(f"  Spec ID: {args.spec_id}")
    print(f"  Spec file: {args.spec_file}")
    print(f"  Version: {args.version}")
    print()
    
    try:
        # Read the spec file
        spec_content = read_spec_file(args.spec_file)

        # Get existing spec files to find the root file path
        print("Getting existing spec file information...")
        spec_files = get_spec_files(args.spec_id)
        print(f"  Found {len(spec_files)} existing file(s)")

        # Find the root file (or first file if none marked as root)
        root_file = None
        file_exists = False
        for f in spec_files:
            print(f"    - {f.get('path')} (type: {f.get('type', 'unknown')})")
            if f.get('type') == 'ROOT':
                root_file = f.get('path')
                file_exists = True
                break

        if not root_file and spec_files:
            # Use the first file if no root is marked
            root_file = spec_files[0].get('path')
            file_exists = True

        if not root_file:
            # Fallback to the input filename - file doesn't exist yet
            root_file = os.path.basename(args.spec_file)
            file_exists = False
            print(f"  No existing files found, will create: {root_file}")
        else:
            print(f"  Using root file: {root_file}")

        # Update or create the spec file content
        if file_exists:
            print("Updating spec file content...")
            try:
                update_spec_file(args.spec_id, spec_content, root_file)
                print("✓ Spec file updated successfully!")
            except Exception as update_error:
                # If update fails with 404, try creating instead
                if "404" in str(update_error):
                    print(f"  Update failed (file may not exist), trying to create...")
                    create_spec_file(args.spec_id, spec_content, root_file)
                    print("✓ Spec file created successfully!")
                else:
                    raise update_error
        else:
            print("Creating spec file...")
            create_spec_file(args.spec_id, spec_content, root_file)
            print("✓ Spec file created successfully!")
        
        # Optionally update the spec name
        if args.update_name:
            print()
            print(f"Updating spec name to: {spec_name}")
            update_spec_properties(args.spec_id, spec_name)
            print("✓ Spec name updated!")
        
        # Get updated spec info
        spec_info = get_spec_info(args.spec_id)
        
        print()
        print("Spec Details:")
        print(f"  Name: {spec_info.get('name', 'N/A')}")
        print(f"  ID:   {args.spec_id}")
        print(f"  Type: {spec_info.get('type', 'N/A')}")
        
        # Set GitHub outputs
        set_github_output("spec_id", args.spec_id)
        set_github_output("spec_name", spec_info.get('name', ''))
        
        return 0
        
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main())

