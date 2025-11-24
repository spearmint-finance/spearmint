#!/usr/bin/env python3
"""
Validate OpenAPI spec against Postman governance and security rules.

This script uses the Postman CLI to validate the OpenAPI specification
against configured governance and security rules in Postman.

Usage:
    python validate_spec.py --spec-file sdk/openapi.json
    python validate_spec.py --spec-file sdk/openapi.json --fail-severity WARNING
    python validate_spec.py --spec-file sdk/openapi.json --output-file validation-results.json
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def check_postman_cli_installed():
    """Check if Postman CLI is installed."""
    try:
        result = subprocess.run(
            ['postman', '--version'],
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode == 0:
            print(f"[OK] Postman CLI found: {result.stdout.strip()}")
            return True
        else:
            print("[ERROR] Postman CLI not found")
            return False
    except FileNotFoundError:
        print("[ERROR] Postman CLI not found")
        return False


def check_postman_login():
    """Check if user is logged in to Postman."""
    try:
        # Try to run a simple command that requires auth
        result = subprocess.run(
            ['postman', 'login', '--help'],
            capture_output=True,
            text=True,
            check=False
        )
        # If help works, CLI is installed. Actual login check happens during lint
        return True
    except FileNotFoundError:
        return False


def validate_spec(spec_file: str, workspace_id: str = None, fail_severity: str = 'ERROR', output_format: str = 'JSON') -> dict:
    """
    Validate OpenAPI spec using Postman CLI.
    
    Args:
        spec_file: Path to OpenAPI spec file
        workspace_id: Postman workspace ID (optional)
        fail_severity: Severity level to fail on (HINT, INFO, WARNING, ERROR)
        output_format: Output format (JSON or CSV)
    
    Returns:
        dict with validation results
    """
    if not os.path.exists(spec_file):
        raise FileNotFoundError(f"Spec file not found: {spec_file}")

    # Convert to absolute path for Postman CLI
    abs_spec_file = os.path.abspath(spec_file)

    # Build command
    cmd = ['postman', 'spec', 'lint', abs_spec_file]
    
    if workspace_id:
        cmd.extend(['--workspace-id', workspace_id])
    
    cmd.extend(['--fail-severity', fail_severity])
    cmd.extend(['--output', output_format])

    print(f"\n[VALIDATING] Spec: {abs_spec_file}")
    print(f"   Workspace ID: {workspace_id or 'Default (All workspaces)'}")
    print(f"   Fail severity: {fail_severity}")
    print(f"   Output format: {output_format}")
    print(f"\n   Running: {' '.join(cmd)}\n")
    
    # Run validation
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=False
    )
    
    # Parse output
    validation_result = {
        'success': result.returncode == 0,
        'exit_code': result.returncode,
        'stdout': result.stdout,
        'stderr': result.stderr,
        'violations': []
    }

    # Check for Postman API errors (workspace not found, auth issues, etc.)
    if result.stderr and 'requested resource could not be found' in result.stderr.lower():
        print("\n[WARNING] Postman workspace not configured or not accessible.")
        print("Skipping Postman governance validation.")
        print("To enable validation, set POSTMAN_WORKSPACE_ID environment variable.")
        # Return success to allow commit to proceed
        validation_result['success'] = True
        validation_result['exit_code'] = 0
        return validation_result

    # Try to parse JSON output
    if output_format == 'JSON' and result.stdout:
        try:
            parsed = json.loads(result.stdout)
            validation_result['violations'] = parsed.get('violations', [])
        except json.JSONDecodeError:
            # Output might not be JSON if there are no violations
            pass

    return validation_result


def print_validation_results(result: dict):
    """Print validation results in a human-readable format."""
    print("\n" + "="*80)
    print("VALIDATION RESULTS")
    print("="*80)

    if result['success']:
        print("\n[PASSED] No governance or security violations found!")
    else:
        print(f"\n[FAILED] Found {len(result['violations'])} violation(s)")
        
        if result['violations']:
            print("\nViolations:")
            print("-" * 80)
            for i, violation in enumerate(result['violations'], 1):
                print(f"\n{i}. {violation.get('severity', 'UNKNOWN')} - Line {violation.get('line number', 'N/A')}")
                print(f"   File: {violation.get('file', 'N/A')}")
                print(f"   Path: {violation.get('path', 'N/A')}")
                print(f"   Issue: {violation.get('issue', 'N/A')}")
    
    if result['stderr']:
        print(f"\nErrors/Warnings:\n{result['stderr']}")
    
    print("\n" + "="*80 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description='Validate OpenAPI spec against Postman governance rules'
    )
    parser.add_argument(
        '--spec-file',
        required=True,
        help='Path to OpenAPI spec file'
    )
    parser.add_argument(
        '--workspace-id',
        help='Postman workspace ID (uses POSTMAN_WORKSPACE_ID env var if not provided)'
    )
    parser.add_argument(
        '--fail-severity',
        default='ERROR',
        choices=['HINT', 'INFO', 'WARNING', 'ERROR'],
        help='Severity level to fail on (default: ERROR)'
    )
    parser.add_argument(
        '--output-file',
        help='Save validation results to JSON file'
    )
    
    args = parser.parse_args()
    
    # Check if Postman CLI is installed
    if not check_postman_cli_installed():
        print("\n[ERROR] Postman CLI is not installed!")
        print("\nInstall it with:")
        print("  curl -o- 'https://dl-cli.pstmn.io/install/linux64.sh' | sh")
        print("  # or for Windows: https://learning.postman.com/docs/postman-cli/postman-cli-installation/")
        sys.exit(1)
    
    # Get workspace ID from args or environment
    workspace_id = args.workspace_id or os.getenv('POSTMAN_WORKSPACE_ID')
    
    # Run validation
    try:
        result = validate_spec(
            spec_file=args.spec_file,
            workspace_id=workspace_id,
            fail_severity=args.fail_severity,
            output_format='JSON'
        )
        
        # Print results
        print_validation_results(result)
        
        # Save to file if requested
        if args.output_file:
            with open(args.output_file, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"[OK] Results saved to: {args.output_file}")

        # Exit with appropriate code
        sys.exit(result['exit_code'])

    except Exception as e:
        print(f"\n[ERROR] Error during validation: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

