"""
Common utilities for Postman API scripts.
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error

# Postman API base URL
POSTMAN_API_BASE = "https://api.getpostman.com"


def get_api_key() -> str:
    """
    Get the Postman API key from environment variable.
    
    Returns:
        The API key string
        
    Raises:
        SystemExit: If the API key is not set
    """
    api_key = os.getenv('POSTMAN_API_KEY')
    if not api_key:
        print("ERROR: POSTMAN_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)
    return api_key


def make_request(
    method: str,
    path: str,
    data: dict = None,
    api_key: str = None,
    max_retries: int = 5,
    retry_delay: int = 2
) -> dict:
    """
    Make a request to the Postman API with retry logic.
    
    Args:
        method: HTTP method (GET, POST, PUT, PATCH, DELETE)
        path: API path (e.g., "/specs/123")
        data: Optional request body data
        api_key: Optional API key (defaults to env var)
        max_retries: Maximum number of retries on failure
        retry_delay: Initial delay between retries (doubles each retry)
        
    Returns:
        Response data as dictionary
        
    Raises:
        Exception: If the request fails after all retries
    """
    if api_key is None:
        api_key = get_api_key()
    
    url = f"{POSTMAN_API_BASE}{path}"
    
    headers = {
        'X-Api-Key': api_key,
        'Content-Type': 'application/json'
    }
    
    json_data = json.dumps(data).encode('utf-8') if data else None
    
    req = urllib.request.Request(
        url,
        data=json_data,
        headers=headers,
        method=method
    )
    
    current_delay = retry_delay
    
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req) as response:
                response_text = response.read().decode('utf-8')
                if response_text:
                    return json.loads(response_text)
                return {}
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            try:
                error_json = json.loads(error_body)
                error_msg = f"Postman API error (HTTP {e.code}): {error_json}"
            except json.JSONDecodeError:
                error_msg = f"Postman API error (HTTP {e.code}): {error_body}"
            
            # Retry on server errors (5xx)
            if e.code >= 500 and attempt < max_retries - 1:
                print(f"  ⚠️  {error_msg}")
                print(f"  ⏳ Retrying in {current_delay}s... (attempt {attempt + 1}/{max_retries})")
                time.sleep(current_delay)
                current_delay *= 2
                continue
            
            raise Exception(error_msg) from None
        except urllib.error.URLError as e:
            if attempt < max_retries - 1:
                print(f"  ⚠️  Network error: {e.reason}")
                print(f"  ⏳ Retrying in {current_delay}s... (attempt {attempt + 1}/{max_retries})")
                time.sleep(current_delay)
                current_delay *= 2
                continue
            
            raise Exception(f"Network error: {e.reason}") from None


def read_spec_file(spec_file: str) -> str:
    """
    Read and validate an OpenAPI spec file.
    
    Args:
        spec_file: Path to the spec file
        
    Returns:
        Content of the spec file as string
        
    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If JSON is invalid
    """
    if not os.path.exists(spec_file):
        raise FileNotFoundError(f"Spec file not found: {spec_file}")
    
    with open(spec_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if spec_file.endswith('.json'):
        try:
            json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in spec file: {e}") from None
    
    return content


def set_github_output(name: str, value: str):
    """
    Set a GitHub Actions output variable.
    
    Args:
        name: Output variable name
        value: Output variable value
    """
    output_file = os.getenv('GITHUB_OUTPUT')
    if output_file:
        with open(output_file, 'a') as f:
            f.write(f"{name}={value}\n")
        print(f"  GitHub output: {name}={value}")

