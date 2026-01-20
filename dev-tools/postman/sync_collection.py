#!/usr/bin/env python3
"""
Sync a Postman collection with its source OpenAPI spec.

This script triggers a sync between a collection and its linked spec,
ensuring the collection reflects the latest spec changes.

Usage:
    python sync_collection.py \
        --spec-id SPEC_ID \
        --collection-uid COLLECTION_UID

Environment:
    POSTMAN_API_KEY: Postman API key (required)
"""

import argparse
import os
import sys
import time

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from postman.common import get_api_key, make_request, set_github_output


def sync_collection_with_spec(spec_id: str, collection_uid: str) -> dict:
    """
    Sync a collection with its source spec.
    
    This triggers an async sync operation. The response contains a task ID
    that can be polled for completion.
    
    Args:
        spec_id: ID of the spec
        collection_uid: UID of the collection to sync
        
    Returns:
        API response with task information
    """
    response = make_request(
        method='PUT',
        path=f"/specs/{spec_id}/collections/{collection_uid}/sync",
        data={}
    )
    
    return response


def poll_sync_task(spec_id: str, collection_uid: str, task_id: str, timeout: int = 120) -> dict:
    """
    Poll for the completion of a collection sync task.
    
    Args:
        spec_id: ID of the spec
        collection_uid: UID of the collection
        task_id: ID of the sync task
        timeout: Maximum time to wait in seconds
        
    Returns:
        Task status response
        
    Raises:
        Exception: If the task fails or times out
    """
    start_time = time.time()
    poll_interval = 2
    
    while time.time() - start_time < timeout:
        response = make_request(
            method='GET',
            path=f"/specs/{spec_id}/tasks/{task_id}"
        )
        
        status = response.get('status', 'unknown')
        
        if status == 'completed':
            return response
        elif status == 'failed':
            error = response.get('error', 'Unknown error')
            raise Exception(f"Collection sync failed: {error}")
        
        print(f"  ⏳ Sync in progress... (status: {status})")
        time.sleep(poll_interval)
    
    raise Exception(f"Collection sync timed out after {timeout} seconds")


def main():
    parser = argparse.ArgumentParser(
        description="Sync a Postman collection with its source OpenAPI spec"
    )
    parser.add_argument(
        '--spec-id',
        required=True,
        help='ID of the spec'
    )
    parser.add_argument(
        '--collection-uid',
        required=True,
        help='UID of the collection to sync'
    )
    parser.add_argument(
        '--timeout',
        type=int,
        default=120,
        help='Timeout for sync operation in seconds (default: 120)'
    )
    
    args = parser.parse_args()
    
    # Ensure API key is available
    get_api_key()
    
    print(f"Syncing collection with spec...")
    print(f"  Spec ID: {args.spec_id}")
    print(f"  Collection UID: {args.collection_uid}")
    print()
    
    try:
        # Trigger the sync
        print("Triggering sync operation...")
        response = sync_collection_with_spec(args.spec_id, args.collection_uid)
        
        task_id = response.get('taskId')
        if task_id:
            print(f"  Task ID: {task_id}")
            print()
            print("Waiting for sync to complete...")
            poll_sync_task(args.spec_id, args.collection_uid, task_id, args.timeout)
        
        print()
        print("✓ Collection synced successfully!")
        
        # Set GitHub outputs
        set_github_output("collection_uid", args.collection_uid)
        set_github_output("sync_status", "success")
        
        return 0
        
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main())

