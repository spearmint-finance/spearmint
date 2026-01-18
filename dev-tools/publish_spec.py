#!/usr/bin/env python3
"""
Publish an OpenAPI spec to Postman's Spec Hub and generate a collection from it.
This script is designed to run in GitHub Actions when the API version is bumped.

The script:
1. Publishes the OpenAPI spec to Postman's Spec Hub
2. Generates a Postman collection from that spec (using Postman's conversion)
3. This ensures the collection is always in sync with the spec

Usage:
    python publish_spec.py \
        --api-key YOUR_POSTMAN_API_KEY \
        --workspace-id WORKSPACE_ID \
        --spec-file sdk/openapi.json \
        --version 1.0.0 \
        --generate-collection
"""

import json
import os
import sys
import argparse
import urllib.request
import urllib.error
from datetime import datetime
import time


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
    # Postman Spec Hub requires at least one file marked as ROOT for creation.
    # Even single-file specs must include a ROOT file type.
    return {
        "name": spec_name,
        "type": spec_type,
        "files": [
            {
                "path": file_path,
                "content": spec_content,
                "type": "ROOT"
            }
        ]
    }


def generate_collection_from_spec(api_key: str, spec_id: str, collection_name: str) -> dict:
    """
    Generate a Postman collection from a spec in Spec Hub.

    This uses Postman's built-in OpenAPI-to-Collection conversion,
    ensuring the collection stays in sync with the spec.

    Args:
        api_key: Postman API key
        spec_id: ID of the spec in Postman Spec Hub
        collection_name: Name for the generated collection

    Returns:
        Response dictionary with collection info

    Raises:
        Exception: If the API call fails
    """
    # API endpoint for generating a collection from a spec
    url = f"https://api.getpostman.com/specs/{spec_id}/generations"

    payload = {
        "elementType": "collection",
        "name": collection_name,
        "options": {
            "folderStrategy": "Tags",  # Group by OpenAPI tags
            "enableOptionalParameters": True,
            "includeAuthInfoInExample": True,
            "includeDeprecated": False,
            "parametersResolution": "Schema",
            "requestNameSource": "Fallback"
        }
    }

    json_data = json.dumps(payload).encode('utf-8')

    req = urllib.request.Request(
        url,
        data=json_data,
        headers={
            'X-Api-Key': api_key,
            'Content-Type': 'application/json'
        },
        method='POST'
    )

    max_retries = 5
    retry_delay = 2

    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req) as response:
                response_data = json.loads(response.read().decode('utf-8'))
                return response_data
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            try:
                error_json = json.loads(error_body)
                error_msg = f"Postman API error (HTTP {e.code}): {error_json}"
            except json.JSONDecodeError:
                error_msg = f"Postman API error (HTTP {e.code}): {error_body}"

            if e.code >= 500 and attempt < max_retries - 1:
                print(f"  ⚠️  {error_msg}")
                print(f"  ⏳ Retrying in {retry_delay} seconds... (attempt {attempt + 1}/{max_retries})")
                time.sleep(retry_delay)
                retry_delay *= 2
                continue

            raise Exception(error_msg) from None
        except urllib.error.URLError as e:
            if attempt < max_retries - 1:
                print(f"  ⚠️  Network error: {e.reason}")
                print(f"  ⏳ Retrying in {retry_delay} seconds... (attempt {attempt + 1}/{max_retries})")
                time.sleep(retry_delay)
                retry_delay *= 2
                continue

            raise Exception(f"Network error: {e.reason}") from None


def poll_generation_task(api_key: str, spec_id: str, task_id: str, timeout: int = 120) -> dict:
    """
    Poll for the completion of a collection generation task.

    Args:
        api_key: Postman API key
        spec_id: ID of the spec
        task_id: ID of the generation task
        timeout: Maximum time to wait in seconds

    Returns:
        Task status response

    Raises:
        Exception: If the task fails or times out
    """
    url = f"https://api.getpostman.com/specs/{spec_id}/tasks/{task_id}"

    req = urllib.request.Request(
        url,
        headers={'X-Api-Key': api_key},
        method='GET'
    )

    start_time = time.time()
    poll_interval = 2

    while time.time() - start_time < timeout:
        try:
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode('utf-8'))
                status = data.get('status', 'unknown')

                if status == 'completed':
                    return data
                elif status == 'failed':
                    error = data.get('error', 'Unknown error')
                    raise Exception(f"Collection generation failed: {error}")

                # Still processing, wait and retry
                print(f"  ⏳ Generation in progress... (status: {status})")
                time.sleep(poll_interval)

        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            raise Exception(f"Failed to check task status: {error_body}") from None

    raise Exception(f"Collection generation timed out after {timeout} seconds")


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
    
    max_retries = 5
    retry_delay = 2  # Start with 2 seconds
    
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req) as response:
                response_data = json.loads(response.read().decode('utf-8'))
                return response_data
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            try:
                error_json = json.loads(error_body)
                error_msg = f"Postman API error (HTTP {e.code}): {error_json}"
            except json.JSONDecodeError:
                error_msg = f"Postman API error (HTTP {e.code}): {error_body}"
            
            # Retry on server errors (5xx) and connection issues
            if e.code >= 500 and attempt < max_retries - 1:
                print(f"  ⚠️  {error_msg}")
                print(f"  ⏳ Retrying in {retry_delay} seconds... (attempt {attempt + 1}/{max_retries})")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
                continue
            
            raise Exception(error_msg) from None
        except urllib.error.URLError as e:
            # Retry on connection errors
            if attempt < max_retries - 1:
                print(f"  ⚠️  Network error: {e.reason}")
                print(f"  ⏳ Retrying in {retry_delay} seconds... (attempt {attempt + 1}/{max_retries})")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
                continue
            
            raise Exception(f"Network error: {e.reason}") from None


def main():
    parser = argparse.ArgumentParser(
        description="Publish an OpenAPI spec to Postman's Spec Hub and optionally generate a collection"
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
        help='Save spec and collection details to JSON file'
    )
    parser.add_argument(
        '--generate-collection',
        action='store_true',
        help='Generate a Postman collection from the spec after publishing'
    )
    parser.add_argument(
        '--collection-name',
        help='Name for the generated collection (default: "Spearmint API - v{version}")'
    )

    args = parser.parse_args()

    # Get API key from argument or environment variable
    api_key = args.api_key or os.getenv('POSTMAN_API_KEY')
    if not api_key:
        print("ERROR: Postman API key not provided", file=sys.stderr)
        print("  Set POSTMAN_API_KEY environment variable or use --api-key", file=sys.stderr)
        sys.exit(1)

    # Determine names
    current_date = datetime.now().strftime("%b %Y")
    spec_name = args.spec_name or f"Spearmint Finance API - v{args.version} ({current_date})"
    collection_name = args.collection_name or f"Spearmint API - v{args.version} ({current_date})"

    print(f"Publishing OpenAPI spec to Postman Spec Hub...")
    print(f"Spec name: {spec_name}")
    print(f"Spec file: {args.spec_file}")
    print(f"Workspace ID: {args.workspace_id}")
    if args.generate_collection:
        print(f"Generate collection: Yes")
        print(f"Collection name: {collection_name}")
    print()

    try:
        # Step 1: Publish the spec
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

        # Step 2: Generate collection if requested
        collection_info = None
        if args.generate_collection and spec_id != 'N/A':
            print()
            print("Generating Postman collection from spec...")

            gen_response = generate_collection_from_spec(
                api_key=api_key,
                spec_id=spec_id,
                collection_name=collection_name
            )

            # The API returns a task ID for async generation
            task_id = gen_response.get('taskId')
            if task_id:
                print(f"  Task ID: {task_id}")
                task_result = poll_generation_task(api_key, spec_id, task_id)
                collection_info = task_result.get('collection', {})
            else:
                # Synchronous response (if generation was immediate)
                collection_info = gen_response.get('collection', gen_response)

            collection_id = collection_info.get('id', 'N/A')
            collection_uid = collection_info.get('uid', 'N/A')

            print()
            print("✓ Collection generated successfully!")
            print()
            print("Collection Details:")
            print(f"  Name: {collection_name}")
            print(f"  ID:   {collection_id}")
            print(f"  UID:  {collection_uid}")
            print()
            print("Access the collection at:")
            print(f"  https://app.postman.com/workspace/{args.workspace_id}/collection/{collection_id}")

        # Save to file if requested
        if args.output_file:
            output_data = {
                "published_at": datetime.now().isoformat(),
                "version": args.version,
                "spec": response
            }
            if collection_info:
                output_data["collection"] = collection_info

            with open(args.output_file, 'w') as f:
                json.dump(output_data, f, indent=2)
            print()
            print(f"Details saved to: {args.output_file}")

        # Set GitHub Actions outputs
        if os.getenv('GITHUB_OUTPUT'):
            with open(os.getenv('GITHUB_OUTPUT'), 'a') as f:
                f.write(f"spec_id={spec_id}\n")
                f.write(f"spec_name={spec_name_response}\n")
                f.write(f"spec_type={spec_type}\n")
                if collection_info:
                    f.write(f"collection_id={collection_info.get('id', '')}\n")
                    f.write(f"collection_uid={collection_info.get('uid', '')}\n")
                    f.write(f"collection_name={collection_name}\n")
            print()
            print("GitHub Actions outputs set:")
            print(f"  spec_id={spec_id}")
            print(f"  spec_name={spec_name_response}")
            print(f"  spec_type={spec_type}")
            if collection_info:
                print(f"  collection_id={collection_info.get('id', '')}")
                print(f"  collection_uid={collection_info.get('uid', '')}")
                print(f"  collection_name={collection_name}")

        return 0

    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main())

