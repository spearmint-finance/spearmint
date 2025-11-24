#!/usr/bin/env python3
"""
Pre-commit test runner with detailed logging.

This script runs all pre-commit validation tests and generates detailed reports
in the dev-tools/commit-testing-log directory.

Usage:
    python dev-tools/run_precommit_tests.py
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


class PreCommitTestRunner:
    """Runs pre-commit tests and generates detailed reports."""
    
    def __init__(self, log_dir: str = "dev-tools/commit-testing-log"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "tests": [],
            "summary": {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "skipped": 0
            }
        }
    
    def run_test(self, name: str, command: list, description: str = "", timeout: int = 120) -> dict:
        """Run a single test and capture results."""
        print(f"\n{'='*80}")
        print(f"Running: {name}")
        print(f"{'='*80}")

        test_result = {
            "name": name,
            "description": description,
            "command": " ".join(command),
            "status": "unknown",
            "exit_code": None,
            "stdout": "",
            "stderr": "",
            "duration_seconds": 0,
            "timeout": timeout
        }

        start_time = datetime.now()

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,
                timeout=timeout
            )
            
            test_result["exit_code"] = result.returncode
            test_result["stdout"] = result.stdout
            test_result["stderr"] = result.stderr
            
            if result.returncode == 0:
                test_result["status"] = "passed"
                print(f"[PASSED] {name}")
            else:
                test_result["status"] = "failed"
                print(f"[FAILED] {name} (exit code: {result.returncode})")
            
            # Print output
            if result.stdout:
                print("\nStdout:")
                print(result.stdout)
            if result.stderr:
                print("\nStderr:")
                print(result.stderr)
                
        except subprocess.TimeoutExpired:
            test_result["status"] = "failed"
            test_result["stderr"] = f"Test timed out after {timeout} seconds"
            print(f"[FAILED] {name} - Timeout after {timeout} seconds")
        except FileNotFoundError as e:
            test_result["status"] = "failed"
            test_result["stderr"] = f"Command not found: {e}"
            print(f"[FAILED] {name} - Command not found: {e}")
        except Exception as e:
            test_result["status"] = "failed"
            test_result["stderr"] = str(e)
            print(f"[FAILED] {name} - Error: {e}")
        
        end_time = datetime.now()
        test_result["duration_seconds"] = (end_time - start_time).total_seconds()
        
        return test_result
    
    def run_all_tests(self):
        """Run all pre-commit tests."""
        print("\n" + "="*80)
        print("PRE-COMMIT TEST SUITE")
        print("="*80)
        print(f"Timestamp: {self.results['timestamp']}")
        print(f"Log directory: {self.log_dir}")
        print("="*80)
        
        # Test 1: OpenAPI Generation
        test1 = self.run_test(
            name="OpenAPI Generation",
            command=[
                "python",
                "core-api/scripts/api_validation/api_validation.py",
                "--generate",
                "--output", "sdk/openapi.json"
            ],
            description="Generate OpenAPI spec from FastAPI application",
            timeout=60  # 60 seconds should be enough for generation
        )
        self.results["tests"].append(test1)

        # Test 2: OpenAPI Spec Validation (Postman)
        log_file = self.log_dir / f"spec_validation_{self.timestamp}.json"
        test2 = self.run_test(
            name="OpenAPI Spec Validation (Postman)",
            command=[
                "python",
                "dev-tools/validate_spec.py",
                "--spec-file", "sdk/openapi.json",
                "--fail-severity", "WARNING",
                "--output-file", str(log_file)
            ],
            description="Validate OpenAPI spec against Postman governance rules",
            timeout=30  # 30 seconds for validation
        )
        self.results["tests"].append(test2)
        
        # Calculate summary
        for test in self.results["tests"]:
            self.results["summary"]["total"] += 1
            if test["status"] == "passed":
                self.results["summary"]["passed"] += 1
            elif test["status"] == "failed":
                self.results["summary"]["failed"] += 1
            elif test["status"] == "skipped":
                self.results["summary"]["skipped"] += 1

    def save_report(self):
        """Save test results to JSON and markdown files."""
        # Save JSON report
        json_file = self.log_dir / f"test_report_{self.timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2)
        print(f"\n[OK] JSON report saved to: {json_file}")

        # Save Markdown report
        md_file = self.log_dir / f"test_report_{self.timestamp}.md"
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(f"# Pre-Commit Test Report\n\n")
            f.write(f"**Timestamp:** {self.results['timestamp']}\n\n")

            # Summary
            f.write(f"## Summary\n\n")
            f.write(f"- **Total Tests:** {self.results['summary']['total']}\n")
            f.write(f"- **Passed:** {self.results['summary']['passed']}\n")
            f.write(f"- **Failed:** {self.results['summary']['failed']}\n")
            f.write(f"- **Skipped:** {self.results['summary']['skipped']}\n\n")

            # Overall status
            if self.results['summary']['failed'] > 0:
                f.write(f"**Overall Status:** [FAILED]\n\n")
            else:
                f.write(f"**Overall Status:** [PASSED]\n\n")

            # Test details
            f.write(f"## Test Details\n\n")
            for i, test in enumerate(self.results['tests'], 1):
                status_badge = "[PASSED]" if test['status'] == 'passed' else "[FAILED]" if test['status'] == 'failed' else "[SKIPPED]"
                f.write(f"### {i}. {test['name']} {status_badge}\n\n")
                f.write(f"**Status:** {test['status'].upper()}\n\n")
                f.write(f"**Description:** {test['description']}\n\n")
                f.write(f"**Command:** `{test['command']}`\n\n")
                f.write(f"**Duration:** {test['duration_seconds']:.2f} seconds\n\n")
                f.write(f"**Exit Code:** {test['exit_code']}\n\n")

                if test['stdout']:
                    f.write(f"**Output:**\n```\n{test['stdout']}\n```\n\n")

                if test['stderr']:
                    f.write(f"**Errors/Warnings:**\n```\n{test['stderr']}\n```\n\n")

                f.write("---\n\n")

        print(f"[OK] Markdown report saved to: {md_file}")

        # Save latest report (symlink or copy)
        latest_json = self.log_dir / "latest_report.json"
        latest_md = self.log_dir / "latest_report.md"

        # Copy files (Windows-compatible)
        import shutil
        shutil.copy2(json_file, latest_json)
        shutil.copy2(md_file, latest_md)

        print(f"[OK] Latest reports updated")

    def print_summary(self):
        """Print test summary to console."""
        print("\n" + "="*80)
        print("TEST SUMMARY")
        print("="*80)
        print(f"Total Tests:  {self.results['summary']['total']}")
        print(f"Passed:       {self.results['summary']['passed']}")
        print(f"Failed:       {self.results['summary']['failed']}")
        print(f"Skipped:      {self.results['summary']['skipped']}")
        print("="*80)

        if self.results['summary']['failed'] > 0:
            print("\n[FAILED] Some tests failed!")
            return False
        else:
            print("\n[PASSED] All tests passed!")
            return True


def main():
    parser = argparse.ArgumentParser(
        description='Run pre-commit tests with detailed logging'
    )
    parser.add_argument(
        '--log-dir',
        default='dev-tools/commit-testing-log',
        help='Directory to save test logs (default: dev-tools/commit-testing-log)'
    )

    args = parser.parse_args()

    # Run tests
    runner = PreCommitTestRunner(log_dir=args.log_dir)
    runner.run_all_tests()
    runner.save_report()
    success = runner.print_summary()

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()


