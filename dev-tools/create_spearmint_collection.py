#!/usr/bin/env python3
"""
Create a Postman collection for the Spearmint API and SDK.
This script is designed to run in GitHub Actions when the API version is bumped.

Usage:
    python create_spearmint_collection.py \
        --api-key YOUR_POSTMAN_API_KEY \
        --workspace-id WORKSPACE_ID \
        --version 1.0.0
"""

import json
import os
import sys
import argparse
import urllib.request
import urllib.error
from datetime import datetime
import time


def create_collection_payload(version: str, base_url: str = "https://api.spearmint.ai") -> dict:
    """
    Create the Postman collection payload for the Spearmint API.
    
    Args:
        version: API version (e.g., "1.0.0")
        base_url: Base URL for the API
        
    Returns:
        Dictionary representing the collection structure
    """
    # Format: "Spearmint API - v0.0.1 (Nov 2025)"
    current_date = datetime.now().strftime("%b %Y")
    collection_name = f"Spearmint API - v{version} ({current_date})"
    
    return {
        "collection": {
            "info": {
                "name": collection_name,
                "description": f"Spearmint API and SDK v{version} - Automated collection",
                "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
            },
            "variable": [
                {
                    "key": "baseUrl",
                    "value": base_url,
                    "description": "Base URL for the Spearmint API"
                },
                {
                    "key": "apiKey",
                    "value": "",
                    "description": "Your Spearmint API key"
                }
            ],
            "auth": {
                "type": "apikey",
                "apikey": [
                    {
                        "key": "value",
                        "value": "{{apiKey}}"
                    },
                    {
                        "key": "key",
                        "value": "Authorization"
                    },
                    {
                        "key": "in",
                        "value": "header"
                    }
                ]
            },
            "item": [
                {
                    "name": "Accounts",
                    "item": [
                        {
                            "name": "Get Account",
                            "request": {
                                "method": "GET",
                                "url": "{{baseUrl}}/accounts/:accountId",
                                "header": [
                                    {
                                        "key": "Accept",
                                        "value": "application/json"
                                    }
                                ]
                            }
                        },
                        {
                            "name": "List Accounts",
                            "request": {
                                "method": "GET",
                                "url": "{{baseUrl}}/accounts",
                                "header": [
                                    {
                                        "key": "Accept",
                                        "value": "application/json"
                                    }
                                ]
                            }
                        }
                    ]
                },
                {
                    "name": "Users",
                    "item": [
                        {
                            "name": "Get User",
                            "request": {
                                "method": "GET",
                                "url": "{{baseUrl}}/users/:userId",
                                "header": [
                                    {
                                        "key": "Accept",
                                        "value": "application/json"
                                    }
                                ]
                            }
                        },
                        {
                            "name": "List Users",
                            "request": {
                                "method": "GET",
                                "url": "{{baseUrl}}/users",
                                "header": [
                                    {
                                        "key": "Accept",
                                        "value": "application/json"
                                    }
                                ]
                            }
                        },
                        {
                            "name": "Create User",
                            "request": {
                                "method": "POST",
                                "url": "{{baseUrl}}/users",
                                "header": [
                                    {
                                        "key": "Content-Type",
                                        "value": "application/json"
                                    }
                                ],
                                "body": {
                                    "mode": "raw",
                                    "raw": json.dumps({
                                        "email": "user@example.com",
                                        "firstName": "John",
                                        "lastName": "Doe"
                                    }, indent=2)
                                }
                            }
                        },
                        {
                            "name": "Update User",
                            "request": {
                                "method": "PUT",
                                "url": "{{baseUrl}}/users/:userId",
                                "header": [
                                    {
                                        "key": "Content-Type",
                                        "value": "application/json"
                                    }
                                ],
                                "body": {
                                    "mode": "raw",
                                    "raw": json.dumps({
                                        "firstName": "Jane",
                                        "lastName": "Smith"
                                    }, indent=2)
                                }
                            }
                        },
                        {
                            "name": "Delete User",
                            "request": {
                                "method": "DELETE",
                                "url": "{{baseUrl}}/users/:userId"
                            }
                        }
                    ]
                },
                {
                    "name": "Transactions",
                    "item": [
                        {
                            "name": "Get Transaction",
                            "request": {
                                "method": "GET",
                                "url": "{{baseUrl}}/transactions/:transactionId",
                                "header": [
                                    {
                                        "key": "Accept",
                                        "value": "application/json"
                                    }
                                ]
                            }
                        },
                        {
                            "name": "List Transactions",
                            "request": {
                                "method": "GET",
                                "url": "{{baseUrl}}/transactions",
                                "header": [
                                    {
                                        "key": "Accept",
                                        "value": "application/json"
                                    }
                                ]
                            }
                        },
                        {
                            "name": "Create Transaction",
                            "request": {
                                "method": "POST",
                                "url": "{{baseUrl}}/transactions",
                                "header": [
                                    {
                                        "key": "Content-Type",
                                        "value": "application/json"
                                    }
                                ],
                                "body": {
                                    "mode": "raw",
                                    "raw": json.dumps({
                                        "type": "expense",
                                        "amount": 100.00,
                                        "description": "Office supplies",
                                        "date": datetime.now().isoformat()
                                    }, indent=2)
                                }
                            }
                        }
                    ]
                }
            ]
        }
    }


def create_collection(api_key: str, workspace_id: str, version: str, base_url: str = "https://api.spearmint.ai") -> dict:
    """
    Create a collection in Postman via the API.
    
    Args:
        api_key: Postman API key
        workspace_id: Target workspace ID
        version: API version
        base_url: Base URL for the Spearmint API
        
    Returns:
        Response dictionary from Postman API
        
    Raises:
        Exception: If the API call fails
    """
    url = f"https://api.getpostman.com/collections?workspace={workspace_id}"
    payload = create_collection_payload(version, base_url)
    
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
    
    max_retries = 3
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
        description="Create a Spearmint API collection in Postman"
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
        '--version',
        required=True,
        help='API/SDK version (e.g., 1.0.0)'
    )
    parser.add_argument(
        '--base-url',
        default='https://api.spearmint.ai',
        help='Base URL for the API (default: https://api.spearmint.ai)'
    )
    parser.add_argument(
        '--output-file',
        help='Save collection details to JSON file'
    )
    
    args = parser.parse_args()
    
    # Get API key from argument or environment variable
    api_key = args.api_key or os.getenv('POSTMAN_API_KEY')
    if not api_key:
        print("ERROR: Postman API key not provided", file=sys.stderr)
        print("  Set POSTMAN_API_KEY environment variable or use --api-key", file=sys.stderr)
        sys.exit(1)
    
    print(f"Creating Spearmint API collection v{args.version}...")
    print(f"Workspace ID: {args.workspace_id}")
    print(f"Base URL: {args.base_url}")
    print()
    
    try:
        response = create_collection(
            api_key=api_key,
            workspace_id=args.workspace_id,
            version=args.version,
            base_url=args.base_url
        )
        
        collection = response.get('collection', {})
        collection_id = collection.get('id', 'N/A')
        collection_name = collection.get('name', 'N/A')
        collection_uid = collection.get('uid', 'N/A')
        
        print("✓ Collection created successfully!", file=sys.stdout)
        print()
        print("Collection Details:")
        print(f"  Name: {collection_name}")
        print(f"  ID:   {collection_id}")
        print(f"  UID:  {collection_uid}")
        print()
        print("Access the collection at:")
        print(f"  https://app.postman.com/workspace/{args.workspace_id}/collections/{collection_id}")
        
        # Save to file if requested
        if args.output_file:
            output_data = {
                "created_at": datetime.now().isoformat(),
                "version": args.version,
                "collection": collection
            }
            with open(args.output_file, 'w') as f:
                json.dump(output_data, f, indent=2)
            print()
            print(f"Collection details saved to: {args.output_file}")
        
        # Set GitHub Actions outputs
        if os.getenv('GITHUB_OUTPUT'):
            with open(os.getenv('GITHUB_OUTPUT'), 'a') as f:
                f.write(f"collection_id={collection_id}\n")
                f.write(f"collection_name={collection_name}\n")
                f.write(f"collection_uid={collection_uid}\n")
            print()
            print("GitHub Actions outputs set:")
            print(f"  collection_id={collection_id}")
            print(f"  collection_name={collection_name}")
            print(f"  collection_uid={collection_uid}")
        
        return 0
        
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main())
