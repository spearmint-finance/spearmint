#!/usr/bin/env python3
"""
Publish an OpenAPI spec to Postman's Spec Hub.
This script is designed to run in GitHub Actions when the API version is bumped.

Usage:
    python publish_spec.py \
        --api-key YOUR_POSTMAN_API_KEY \
        --workspace-id WORKSPACE_ID \
        --spec-file sdk/openapi.json \
        --version 1.0.0
"""

import json
import os
import sys
import argparse
import urllib.request
import urllib.error
from datetime import datetime


def read_openapi_spec(spec_file: str) -> str:
    """
    Read the OpenAPI spec file and return it as a string.
    
    Args:
        spec_file: Path to the OpenAPI spec file (JSON or YAML)
        
    Returns:
        String content of the spec file
        
    Raises:
        FileNotFoundError: If the spec file doesn't exist
    """
    if not os.path.exists(spec_file):
        raise FileNotFoundError(f"Spec file not found: {spec_file}")
    
    with open(spec_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Validate it's valid JSON if it's a .json file
    if spec_file.endswith('.json'):
        try:
            json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in spec file: {e}") from None
    
    return content


def detect_spec_type(spec_file: str, content: str) -> str:
    """
    Detect the OpenAPI spec type from the file content.
    
    Args:
        spec_file: Path to the spec file
        content: Content of the spec file
        
    Returns:
        Spec type string (e.g., "OPENAPI:3.0", "OPENAPI:3.1")
    """
    # Try to parse as JSON
    try:
        spec_data = json.loads(content)
        openapi_version = spec_data.get('openapi', '')
        
        if openapi_version.startswith('3.1'):
            return 'OPENAPI:3.1'
        elif openapi_version.startswith('3.0'):
            return 'OPENAPI:3.0'
        elif spec_data.get('swagger') == '2.0':
            return 'OPENAPI:2.0'
    except json.JSONDecodeError:
        # If not JSON, assume YAML
        if 'openapi: 3.1' in content or 'openapi: "3.1' in content:
            return 'OPENAPI:3.1'
        elif 'openapi: 3.0' in content or 'openapi: "3.0' in content:
            return 'OPENAPI:3.0'
        elif 'swagger: 2.0' in content or 'swagger: "2.0' in content:
            return 'OPENAPI:2.0'
    
    # Default to OpenAPI 3.0
    return 'OPENAPI:3.0'


def create_spec_payload(spec_name: str, spec_type: str, spec_content: str, file_path: str) -> dict:
    """
    Create the payload for creating a spec in Postman.
    
    Args:
        spec_name: Name of the spec
        spec_type: Type of spec (e.g., "OPENAPI:3.0")
        spec_content: Content of the spec file as a string
        file_path: File path for the spec (e.g., "openapi.json")
        
    Returns:
        Dictionary representing the spec creation payload
    """
    return {
        "name": spec_name,
        "type": spec_type,
        "files": [
            {
                "path": file_path,
                "content": spec_content
            }
        ]
    }


def publish_spec(api_key: str, workspace_id: str, spec_name: str, spec_file: str) -> dict:
    """
    Publish a spec to Postman's Spec Hub.
    
    Args:
        api_key: Postman API key
        workspace_id: Target workspace ID
        spec_name: Name for the spec
        spec_file: Path to the OpenAPI spec file
        
    Returns:
        Response dictionary from Postman API
        
    Raises:
        Exception: If the API call fails
    """
    # Read the spec file
    spec_content = read_openapi_spec(spec_file)
    
    # Detect spec type
    spec_type = detect_spec_type(spec_file, spec_content)
    
    # Determine file path (use basename)
    file_path = os.path.basename(spec_file)
    
    # Create payload
    payload = create_spec_payload(spec_name, spec_type, spec_content, file_path)
    
    # API endpoint
    url = f"https://api.getpostman.com/specs?workspaceId={workspace_id}"
    
    # Convert to JSON
    json_data = json.dumps(payload).encode('utf-8')
    
    # Create request
    req = urllib.request.Request(
        url,
        data=json_data,
        headers={
            'X-Api-Key': api_key,
            'Content-Type': 'application/json'
        },
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            response_data = json.loads(response.read().decode('utf-8'))
            return response_data
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        try:
            error_json = json.loads(error_body)
            raise Exception(f"Postman API error (HTTP {e.code}): {error_json}") from None
        except json.JSONDecodeError:
            raise Exception(f"Postman API error (HTTP {e.code}): {error_body}") from None
    except urllib.error.URLError as e:
        raise Exception(f"Network error: {e.reason}") from None


def main():
    parser = argparse.ArgumentParser(
        description="Publish an OpenAPI spec to Postman's Spec Hub"
    )
    parser.add_argument(
        '--api-key',
        required=False,
        help='Postman API key (default: POSTMAN_API_KEY env var)'
    )
    parser.add_argument(
        '--workspace-id',
        required=True,
        help='Postman workspace ID'
    )
    parser.add_argument(
        '--spec-file',
        required=True,
        help='Path to OpenAPI spec file (JSON or YAML)'
    )
    parser.add_argument(
        '--version',
        required=True,
        help='API version (e.g., 1.0.0)'
    )
    parser.add_argument(
        '--spec-name',
        help='Name for the spec (default: "Spearmint Finance API - v{version}")'
    )
    parser.add_argument(
        '--output-file',
        help='Save spec details to JSON file'
    )

    args = parser.parse_args()

    # Get API key from argument or environment variable
    api_key = args.api_key or os.getenv('POSTMAN_API_KEY')
    if not api_key:
        print("ERROR: Postman API key not provided", file=sys.stderr)
        print("  Set POSTMAN_API_KEY environment variable or use --api-key", file=sys.stderr)
        sys.exit(1)

    # Determine spec name
    current_date = datetime.now().strftime("%b %Y")
    spec_name = args.spec_name or f"Spearmint Finance API - v{args.version} ({current_date})"

    print(f"Publishing OpenAPI spec to Postman Spec Hub...")
    print(f"Spec name: {spec_name}")
    print(f"Spec file: {args.spec_file}")
    print(f"Workspace ID: {args.workspace_id}")
    print()

    try:
        response = publish_spec(
            api_key=api_key,
            workspace_id=args.workspace_id,
            spec_name=spec_name,
            spec_file=args.spec_file
        )

        spec_id = response.get('id', 'N/A')
        spec_name_response = response.get('name', 'N/A')
        spec_type = response.get('type', 'N/A')
        created_at = response.get('createdAt', 'N/A')

        print("✓ Spec published successfully!", file=sys.stdout)
        print()
        print("Spec Details:")
        print(f"  Name:       {spec_name_response}")
        print(f"  ID:         {spec_id}")
        print(f"  Type:       {spec_type}")
        print(f"  Created At: {created_at}")
        print()
        print("Access the spec at:")
        print(f"  https://app.postman.com/workspace/{args.workspace_id}/specs/{spec_id}")

        # Save to file if requested
        if args.output_file:
            output_data = {
                "published_at": datetime.now().isoformat(),
                "version": args.version,
                "spec": response
            }
            with open(args.output_file, 'w') as f:
                json.dump(output_data, f, indent=2)
            print()
            print(f"Spec details saved to: {args.output_file}")

        # Set GitHub Actions outputs
        if os.getenv('GITHUB_OUTPUT'):
            with open(os.getenv('GITHUB_OUTPUT'), 'a') as f:
                f.write(f"spec_id={spec_id}\n")
                f.write(f"spec_name={spec_name_response}\n")
                f.write(f"spec_type={spec_type}\n")
            print()
            print("GitHub Actions outputs set:")
            print(f"  spec_id={spec_id}")
            print(f"  spec_name={spec_name_response}")
            print(f"  spec_type={spec_type}")

        return 0

    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main())

