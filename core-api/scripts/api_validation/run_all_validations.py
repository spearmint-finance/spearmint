#!/usr/bin/env python3
"""
API Validation Test Runner

This script runs all API validation tests (structural, Spectral, Postman) and
generates detailed reports in the core-api/scripts/api_validation/logs directory.

This is the main orchestrator for:
- OpenAPI structural validation
- Spectral linting (100+ Google API Design rules)
- Postman governance validation

Usage:
    python core-api/scripts/api_validation/run_all_validations.py
    python core-api/scripts/api_validation/run_all_validations.py --verbose
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from core-api/.env
load_dotenv(dotenv_path=Path(__file__).parent.parent.parent / ".env")


class PreCommitTestRunner:
    """Runs pre-commit tests and generates detailed reports.

    Behavior change: Spectral errors now ALWAYS fail the suite (previously
    gated behind --fail-on-spectral-error). The flag has been removed for
    simplicity and policy enforcement.
    """

    def __init__(self, log_dir: str = "core-api/scripts/api_validation/logs", verbose: bool = False, summary_only: bool = False):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.verbose = verbose
        self.summary_only = summary_only
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
        # Use ASCII characters for Windows compatibility
        self.spinner_chars = ['|', '/', '-', '\\']
        self.spinner_idx = 0
    
    def show_progress(self, message: str):
        """Show a spinner progress indicator."""
        if not self.verbose:
            self.spinner_idx = (self.spinner_idx + 1) % len(self.spinner_chars)
            spinner = self.spinner_chars[self.spinner_idx]
            # Use \r to overwrite the line
            print(f"\r{spinner} {message}...", end='', flush=True)

    def run_test(self, name: str, command: list, description: str = "", timeout: int = 120, artifact_file: str | None = None) -> dict:
        """Run a single test and capture results."""
        if self.verbose:
            print(f"\n{'='*80}")
            print(f"Running: {name}")
            print(f"{'='*80}")
        else:
            # Just show a simple progress message
            print(f"\r{self.spinner_chars[0]} Running: {name}...", end='', flush=True)

        test_result = {
            "name": name,
            "description": description,
            "command": " ".join(command),
            "status": "unknown",
            "exit_code": None,
            "stdout": "",
            "stderr": "",
            "duration_seconds": 0,
            "timeout": timeout,
            # Allow callers to pre-attach an artifact path (e.g., Postman JSON)
            "artifact_file": artifact_file
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
                if self.verbose:
                    print(f"[PASSED] {name}")
                else:
                    # Skip inline status in summary mode for Full Pipeline (will print after Spectral check)
                    if "Full Pipeline" not in name:
                        if self.summary_only:
                            passed_ct, failed_ct, warn_ct = self._compute_brief_counts(name, test_result)
                            print(f"\r[OK] {name} - {passed_ct}# PASSED | {failed_ct}# FAILED | {warn_ct}# WARNINGS                    ")
                        else:
                            print(f"\r[OK] {name}                    ")
            else:
                test_result["status"] = "failed"
                if self.verbose:
                    print(f"[FAILED] {name} (exit code: {result.returncode})")
                else:
                    if self.summary_only:
                        passed_ct, failed_ct, warn_ct = self._compute_brief_counts(name, test_result)
                        print(f"\r[FAILED] {name} - {passed_ct}# PASSED | {failed_ct}# FAILED | {warn_ct}# WARNINGS                    ")
                    else:
                        print(f"\r[FAILED] {name} (exit code: {result.returncode})                    ")

            # Print output only in verbose mode
            if self.verbose:
                if result.stdout:
                    print("\nStdout:")
                    print(result.stdout)
                if result.stderr:
                    print("\nStderr:")
                    print(result.stderr)
                
        except subprocess.TimeoutExpired:
            test_result["status"] = "failed"
            test_result["stderr"] = f"Test timed out after {timeout} seconds"
            if self.verbose:
                print(f"[FAILED] {name} - Timeout after {timeout} seconds")
            else:
                print(f"\r[FAILED] {name} - Timeout                    ")
        except FileNotFoundError as e:
            test_result["status"] = "failed"
            test_result["stderr"] = f"Command not found: {e}"
            if self.verbose:
                print(f"[FAILED] {name} - Command not found: {e}")
            else:
                print(f"\r[FAILED] {name} - Command not found                    ")
        except Exception as e:
            test_result["status"] = "failed"
            test_result["stderr"] = str(e)
            if self.verbose:
                print(f"[FAILED] {name} - Error: {e}")
            else:
                print(f"\r[FAILED] {name} - Error                    ")
        
        end_time = datetime.now()
        test_result["duration_seconds"] = (end_time - start_time).total_seconds()
        
        return test_result

    def _compute_brief_counts(self, test_name: str, test_result: dict) -> tuple[int, int, int]:
        """Return (passed_count, failed_count, warnings_count) for a single high-level test.

        Rules:
        - For "Full Pipeline": parse per-step PASS/FAIL lines from api_validation output
          to count actual sub-steps (Structural before, Bundling, Spectral, Structural after).
        - For "Postman Governance": compute failures by counting violations at or above the
          fail severity when available; warnings_count counts WARNING severity. We cannot
          reliably infer total passed rule checks from Postman CLI JSON output, so passed
          will be 1 when the overall run succeeded, else 0.
        """
        passed_ct = 1 if test_result.get("status") == "passed" else 0
        failed_ct = 1 if test_result.get("status") == "failed" else 0
        warnings_ct = 0

        stdout = test_result.get("stdout") or ""
        stderr = test_result.get("stderr") or ""
        combined = "\n".join([stdout, stderr])

        # For the full pipeline test, parse per-step PASS/FAIL summary and Spectral warnings
        if "Full Pipeline" in test_name:
            per_step_pass = 0
            per_step_fail = 0
            # Example line: Spectral summary: ✖ 760 problems (12 errors, 748 warnings, 0 infos, 0 hints)
            for line in combined.splitlines():
                # Count step results from "Validation Summary" section in api_validation.py output
                if "PASS:" in line:
                    per_step_pass += 1
                elif "FAIL:" in line:
                    per_step_fail += 1
                if "Spectral summary:" in line:
                    m = re.search(r"\((\d+) errors,\s*(\d+) warnings", line)
                    if m:
                        try:
                            warnings_ct = int(m.group(2))
                        except ValueError:
                            warnings_ct = 0
                    # don't break; continue scanning for per-step lines too
            # If we found any per-step counts, prefer them over default 1/0
            if per_step_pass or per_step_fail:
                passed_ct = per_step_pass
                failed_ct = per_step_fail

        # For Postman governance, try to read violations from saved artifact JSON
        if "Postman Governance" in test_name:
            artifact = test_result.get("artifact_file")
            if artifact and Path(artifact).exists():
                try:
                    with open(artifact, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    violations = data.get('violations', []) or []
                    # Count warnings (case-insensitive match on 'severity')
                    warnings_ct = sum(1 for v in violations if str(v.get('severity', '')).upper() == 'WARNING')
                    # Compute failures as violations at or above fail severity threshold if we can infer it
                    # Default to ERROR threshold (matches orchestrator command)
                    fail_levels = {"HINT": 0, "INFO": 1, "WARNING": 2, "ERROR": 3}
                    threshold = 3  # ERROR
                    failed_ct = sum(1 for v in violations if fail_levels.get(str(v.get('severity', '')).upper(), -1) >= threshold)
                    # We cannot infer the total number of rule checks executed from Postman JSON,
                    # so treat "passed" as overall run success (1/0) when no failures.
                    passed_ct = 1 if (test_result.get("status") == "passed") else 0
                except Exception:
                    warnings_ct = warnings_ct or 0
        return passed_ct, failed_ct, warnings_ct
    
    def run_all_tests(self):
        """Run all pre-commit tests."""
        if self.verbose:
            print("\n" + "="*80)
            print("PRE-COMMIT TEST SUITE")
            print("="*80)
            print(f"Timestamp: {self.results['timestamp']}")
            print(f"Log directory: {self.log_dir}")
            print("="*80)
        else:
            # Compact header for non-verbose mode
            print("\nRunning pre-commit tests...")

        # Test 1: OpenAPI Spec Validation (Full Pipeline)
        # This mimics the CI/CD workflow and runs:
        # 1. Structural validation (OpenAPI schema compliance)
        # 2. Bundling external refs
        # 3. Spectral linting (100+ Google API Design rules)
        # 4. Post-bundle structural validation

        # Get repository root (3 levels up from this script)
        repo_root = Path(__file__).parent.parent.parent.parent

        pipeline_command = [
            "python",
            str(repo_root / "core-api" / "scripts" / "api_validation" / "api_validation.py"),
            "--file", str(repo_root / "sdk" / "openapi.json"),
        ]
        if self.summary_only:
            pipeline_command.append("--summary-only")

        test1 = self.run_test(
            name="OpenAPI Spec Validation (Full Pipeline)",
            command=pipeline_command,
            description="Validate OpenAPI spec: structure, bundling, Spectral linting (100+ rules), post-bundle validation",
            timeout=60  # 60 seconds for full validation pipeline
        )

        # Always evaluate Spectral summary and fail if errors > 0 (policy enforcement)
        spectral_summary = self._extract_spectral_summary(test1["stdout"], test1["stderr"])
        if spectral_summary:
            test1["spectral_problems"] = spectral_summary.get("problems")
            test1["spectral_errors"] = spectral_summary.get("errors")
            test1["spectral_warnings"] = spectral_summary.get("warnings")
            if test1["status"] == "passed" and spectral_summary.get("errors", 0) > 0:
                test1["status"] = "failed"
                test1["stderr"] += f"\nSpectral errors detected ({spectral_summary['errors']}); failing (policy)"
                # Now print the final status line (we skipped it earlier for Full Pipeline)
                if self.verbose:
                    print(f"[FAILED] {test1['name']} - Spectral errors: {spectral_summary['errors']}")
                else:
                    if self.summary_only:
                        # Compute counts but override failed count with Spectral errors
                        passed_ct, _, warn_ct = self._compute_brief_counts(test1['name'], test1)
                        print(f"\r[FAILED] {test1['name']} - {passed_ct}# PASSED | {spectral_summary['errors']}# ERRORS | {warn_ct}# WARNINGS                    ")
                    else:
                        print(f"\r[FAILED] {test1['name']} - Spectral errors: {spectral_summary['errors']}                    ")
            else:
                # No errors or already failed; print deferred status line for Full Pipeline
                if not self.verbose and test1["status"] == "passed":
                    if self.summary_only:
                        passed_ct, failed_ct, warn_ct = self._compute_brief_counts(test1['name'], test1)
                        print(f"\r[OK] {test1['name']} - {passed_ct}# PASSED | {failed_ct}# FAILED | {warn_ct}# WARNINGS                    ")
                    else:
                        print(f"\r[OK] {test1['name']}                    ")
        else:
            # No Spectral summary found; print deferred status line for Full Pipeline
            if not self.verbose and test1["status"] == "passed":
                if self.summary_only:
                    passed_ct, failed_ct, warn_ct = self._compute_brief_counts(test1['name'], test1)
                    print(f"\r[OK] {test1['name']} - {passed_ct}# PASSED | {failed_ct}# FAILED | {warn_ct}# WARNINGS                    ")
                else:
                    print(f"\r[OK] {test1['name']}                    ")
        self.results["tests"].append(test1)

        # Test 2: OpenAPI Spec Validation (Postman Governance)
        # This mimics the CI/CD workflow Postman validation step
        # Only runs if POSTMAN_WORKSPACE_ID is set
        workspace_id = os.environ.get('POSTMAN_WORKSPACE_ID')

        if workspace_id:
            log_file = self.log_dir / f"spec_validation_{self.timestamp}.json"
            postman_command = [
                "python",
                str(repo_root / "core-api" / "scripts" / "api_validation" / "postman_validation.py"),
                "--spec-file", str(repo_root / "sdk" / "openapi.json"),
                "--workspace-id", workspace_id,
                "--fail-severity", "ERROR",  # Match CI/CD severity
                "--output-file", str(log_file),
            ]
            if self.summary_only:
                postman_command.append("--summary-only")
            test2 = self.run_test(
                name="OpenAPI Spec Validation (Postman Governance)",
                command=postman_command,
                description="Validate OpenAPI spec against Postman governance and security rules",
                timeout=300,  # 5 minutes for validation (large spec file)
                artifact_file=str(log_file)
            )
            # Artifact already attached above; keep for completeness
            self.results["tests"].append(test2)
        else:
            # Skip Postman validation if workspace ID not set
            if self.verbose:
                print("\n[SKIPPED] Postman validation - POSTMAN_WORKSPACE_ID not set")
                print("To enable: Set POSTMAN_WORKSPACE_ID environment variable")
            else:
                print("\r[SKIPPED] Postman validation - POSTMAN_WORKSPACE_ID not set")

            self.results["tests"].append({
                "name": "OpenAPI Spec Validation (Postman Governance)",
                "description": "Validate OpenAPI spec against Postman governance and security rules",
                "command": "skipped - POSTMAN_WORKSPACE_ID not set",
                "status": "skipped",
                "exit_code": None,
                "stdout": "Skipped: POSTMAN_WORKSPACE_ID environment variable not set",
                "stderr": "",
                "duration_seconds": 0,
                "timeout": 30
            })

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
        if self.verbose:
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

        if self.verbose:
            print(f"[OK] Markdown report saved to: {md_file}")

        # Save latest report (symlink or copy)
        latest_json = self.log_dir / "latest_report.json"
        latest_md = self.log_dir / "latest_report.md"

        # Copy files (Windows-compatible)
        import shutil
        shutil.copy2(json_file, latest_json)
        shutil.copy2(md_file, latest_md)

        if self.verbose:
            print(f"[OK] Latest reports updated")

    def print_summary(self):
        """Print test summary to console, including Spectral counts."""
        # Fetch spectral stats from first test if available
        spectral_errors = None
        spectral_warnings = None
        spectral_problems = None
        for t in self.results.get("tests", []):
            if "spectral_errors" in t:
                spectral_errors = t.get("spectral_errors")
                spectral_warnings = t.get("spectral_warnings")
                spectral_problems = t.get("spectral_problems")
                break

        if self.verbose:
            print("\n" + "="*80)
            print("TEST SUMMARY")
            print("="*80)
            print(f"Total Tests:  {self.results['summary']['total']}")
            print(f"Passed:       {self.results['summary']['passed']}")
            print(f"Failed:       {self.results['summary']['failed']}")
            print(f"Skipped:      {self.results['summary']['skipped']}")
            if spectral_errors is not None:
                print("-"*80)
                print(f"Spectral: {spectral_errors} errors, {spectral_warnings} warnings (problems: {spectral_problems})")
            print("="*80)
        else:
            passed = self.results['summary']['passed']
            total = self.results['summary']['total']
            print(f"\n{passed}/{total} tests passed")
            if spectral_errors is not None:
                print(f"Spectral: {spectral_errors} errors, {spectral_warnings} warnings")

        if self.results['summary']['failed'] > 0:
            if self.verbose:
                print("\n[FAILED] Some tests failed!")
            else:
                print("[FAILED] Some tests failed")
            return False
        else:
            if self.verbose:
                print("\n[PASSED] All tests passed!")
            else:
                print("[PASSED] All tests passed")
            return True

    def _extract_spectral_summary(self, stdout: str, stderr: str) -> dict | None:
        """Extract Spectral summary metrics: problems, errors, warnings.

        Returns dict {problems, errors, warnings} or None if not found.
        """
        combined = "\n".join([stdout or "", stderr or ""])
        for line in combined.splitlines():
            if "problems" in line and "errors" in line and "warnings" in line:
                # Normalize line (strip leading label like 'Spectral summary:')
                summary_part = line.split(":", 1)[-1].strip() if ":" in line else line.strip()
                # Regex capture
                m = re.search(r"(\d+)\s+problems\s*\(\s*(\d+)\s+errors,\s*(\d+)\s+warnings", summary_part)
                if m:
                    try:
                        return {
                            "problems": int(m.group(1)),
                            "errors": int(m.group(2)),
                            "warnings": int(m.group(3)),
                        }
                    except ValueError:
                        return None
        return None


def main():
    parser = argparse.ArgumentParser(
        description='Run API validation tests with detailed logging'
    )
    parser.add_argument(
        '--log-dir',
        default='core-api/scripts/api_validation/logs',
        help='Directory to save test logs (default: core-api/scripts/api_validation/logs)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed output (default: compact mode with progress indicators)'
    )

    parser.add_argument(
        '--summary-only',
        action='store_true',
        help='Suppress detailed Spectral/Postman outputs and show only summary lines'
    )
    args = parser.parse_args()

    # Run tests
    runner = PreCommitTestRunner(
        log_dir=args.log_dir,
        verbose=args.verbose,
        summary_only=args.summary_only,
    )
    runner.run_all_tests()
    runner.save_report()
    success = runner.print_summary()

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()


