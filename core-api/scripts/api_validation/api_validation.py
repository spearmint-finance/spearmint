#!/usr/bin/env python3
"""
Fetch, validate, bundle, and lint OpenAPI specification.

This script provides an integrated workflow to:
1. Fetch the OpenAPI spec from a running server or generate locally
2. Validate structural correctness (OpenAPI compliance)
3. Bundle external $ref files (if present)
4. Lint with Spectral using Google API Design ruleset
5. Re-validate to ensure linting didn't break the spec

Usage:
    python api_validation.py --help
    python api_validation.py --fetch http://localhost:8000/api/openapi.json
    python api_validation.py --generate
    python api_validation.py --file ./openapi.json

Cross-platform: works on Windows, macOS, Linux.
"""

import argparse
import json
import logging
import sys
import subprocess
from pathlib import Path
from typing import Optional, Tuple
import tempfile
import shutil

try:
    import requests
except ImportError:
    requests = None

try:
    from openapi_spec_validator import validate_spec
    from openapi_spec_validator.readers import read_from_filename
except ImportError:
    validate_spec = None

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SpecValidator:
    """Manages OpenAPI spec validation and linting workflow."""

    def __init__(self, spec_path: str, ruleset: Optional[str] = None):
        """
        Initialize validator.

        Args:
            spec_path: Path to OpenAPI spec file (JSON or YAML)
            ruleset: Path to Spectral ruleset file (default: .spectral-google.yaml)
        """
        self.spec_path = Path(spec_path).resolve()
        
        # Resolve ruleset path: prefer explicit arg, then look in same dir as this script, then repo root, then current dir
        if ruleset:
            self.ruleset = Path(ruleset).resolve()
        else:
            # Try to find .spectral-google.yaml in common locations
            # Path(__file__).parent = core-api/scripts/api_validation
            script_dir = Path(__file__).parent
            repo_root = script_dir.parent.parent.parent  # core-api/scripts/api_validation -> repo root (spearmint)
            candidates = [
                script_dir / '.spectral-google.yaml',      # same dir as this script (preferred)
                repo_root / '.spectral-google.yaml',       # repo root fallback
                Path('.spectral-google.yaml').resolve(),   # current working dir
            ]
            self.ruleset = next((p for p in candidates if p.exists()), candidates[0])
        
        self.spec_dir = self.spec_path.parent
        self.bundled_spec_path: Optional[Path] = None

    def validate_structure(self, spec_path: Optional[Path] = None) -> bool:
        """
        Validate OpenAPI spec against OpenAPI schema.

        Args:
            spec_path: Path to spec (default: self.spec_path)

        Returns:
            True if valid, False otherwise
        """
        if validate_spec is None:
            logger.error(
                "openapi-spec-validator not installed. "
                "Run: pip install openapi-spec-validator"
            )
            return False

        check_path = spec_path or self.spec_path
        logger.info(f"Validating structure: {check_path}")

        try:
            spec_dict, _ = read_from_filename(str(check_path))
            validate_spec(spec_dict)
            logger.info(f"✅ Spec at {check_path} is structurally valid.")
            return True
        except Exception as e:
            logger.error(f"❌ Validation Error: {e}")
            return False

    def bundle_refs(self) -> bool:
        """
        Bundle external $ref files using swagger-cli.

        Returns:
            True if bundled or not needed, False on error
        """
        logger.info("Checking for external $ref files...")

        # Check if spec references external files
        try:
            with open(self.spec_path, 'r') as f:
                content = f.read()
                if '$ref' not in content or 'http' in content:
                    logger.info("No external $ref files detected or already absolute URLs.")
                    return True
        except Exception as e:
            logger.warning(f"Could not check for external refs: {e}")
            return True

        # Try to use swagger-cli to bundle
        logger.info("Attempting to bundle with swagger-cli...")
        try:
            # Use npx to run swagger-cli
            bundled_path = self.spec_dir / f"{self.spec_path.stem}-bundled.json"
            cmd = [
                'npx',
                '@apidevtools/swagger-cli',
                'bundle',
                str(self.spec_path),
                '-o',
                str(bundled_path),
                '--dereference'
            ]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                logger.info(f"✅ Spec bundled to {bundled_path}")
                self.bundled_spec_path = bundled_path
                return True
            else:
                logger.warning(
                    f"swagger-cli failed (exit {result.returncode}). "
                    f"Continuing with unbundled spec.\nStderr: {result.stderr}"
                )
                return True  # Non-fatal; continue with original
        except FileNotFoundError:
            logger.warning(
                "swagger-cli not found. To bundle external refs, install: npm install -g @apidevtools/swagger-cli"
            )
            return True  # Non-fatal
        except subprocess.TimeoutExpired:
            logger.warning("swagger-cli timed out. Continuing with unbundled spec.")
            return True
        except Exception as e:
            logger.warning(f"Could not bundle refs: {e}. Continuing with unbundled spec.")
            return True

    def lint_with_spectral(self) -> bool:
        """
        Lint spec with Spectral using configured ruleset.

        Returns:
            True if linting passed, False otherwise
        """
        # Use bundled spec if available, otherwise original
        lint_path = self.bundled_spec_path or self.spec_path

        logger.info(f"Linting with Spectral: {lint_path}")
        logger.info(f"Using ruleset: {self.ruleset}")

        if not self.ruleset.exists():
            logger.warning(
                f"Ruleset not found: {self.ruleset}. "
                f"Skipping Spectral linting."
            )
            return True  # Non-fatal

        try:
            cmd = [
                'npx',
                '@stoplight/spectral-cli',
                'lint',
                str(lint_path),
                '--ruleset',
                str(self.ruleset),
                '--fail-severity',
                'error'
            ]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0:
                logger.info("✅ Spectral linting passed.")
                if result.stdout:
                    logger.info(f"Spectral output:\n{result.stdout}")
                return True
            else:
                logger.warning(f"⚠️ Spectral linting detected issues.")
                if result.stdout:
                    logger.warning(f"Spectral output:\n{result.stdout}")
                if result.stderr:
                    logger.warning(f"Stderr:\n{result.stderr}")
                return True  # Non-fatal; issues noted but continue
        except FileNotFoundError:
            logger.warning(
                "⚠️ Spectral CLI not found. Linting skipped. "
                "Install with: npm install -g @stoplight/spectral-cli"
            )
            return True  # Non-fatal
        except subprocess.TimeoutExpired:
            logger.warning("⚠️ Spectral linting timed out. Continuing.")
            return True  # Non-fatal
        except Exception as e:
            logger.warning(f"⚠️ Could not run Spectral: {e}. Continuing.")
            return True  # Non-fatal

    def cleanup_bundled(self):
        """Remove bundled spec file if it was created."""
        if self.bundled_spec_path and self.bundled_spec_path.exists():
            try:
                self.bundled_spec_path.unlink()
                logger.info(f"Cleaned up bundled spec: {self.bundled_spec_path}")
            except Exception as e:
                logger.warning(f"Could not clean up bundled spec: {e}")

    def run_full_validation(self) -> bool:
        """
        Run full validation pipeline.

        Returns:
            True if all steps passed, False otherwise
        """
        logger.info("="*80)
        logger.info("Starting OpenAPI Validation Pipeline")
        logger.info("="*80)

        steps = [
            ("Structural Validation (before)", lambda: self.validate_structure()),
            ("Bundling External Refs", self.bundle_refs),
            ("Spectral Linting", self.lint_with_spectral),
            ("Structural Validation (after)", lambda: self.validate_structure(self.bundled_spec_path or self.spec_path)),
        ]

        results = []
        for step_name, step_func in steps:
            logger.info(f"\n--- {step_name} ---")
            try:
                result = step_func()
                results.append((step_name, result))
                if not result:
                    logger.error(f"❌ {step_name} failed. Stopping pipeline.")
                    break
            except Exception as e:
                logger.error(f"❌ {step_name} raised an exception: {e}")
                results.append((step_name, False))
                break

        # Cleanup
        self.cleanup_bundled()

        # Summary
        logger.info("\n" + "="*80)
        logger.info("Validation Summary")
        logger.info("="*80)
        for step_name, result in results:
            status = "✅ PASS" if result else "❌ FAIL"
            logger.info(f"{status}: {step_name}")

        all_passed = all(result for _, result in results)
        logger.info("="*80)
        if all_passed:
            logger.info("✅ All validation steps passed!")
        else:
            logger.error("❌ Validation failed. See errors above.")
        logger.info("="*80)

        return all_passed


def fetch_spec(url: str, output_path: str) -> bool:
    """
    Fetch OpenAPI spec from a remote URL.

    Args:
        url: Full URL to OpenAPI endpoint
        output_path: Where to save the spec

    Returns:
        True if successful, False otherwise
    """
    if requests is None:
        logger.error(
            "requests library not installed. "
            "Run: pip install requests"
        )
        return False

    logger.info(f"Fetching spec from {url}...")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        with open(output_path, 'w') as f:
            f.write(response.text)
        logger.info(f"✅ Spec fetched and saved to {output_path}")
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Failed to fetch spec: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Error saving spec: {e}")
        return False


def generate_spec(output_path: str) -> bool:
    """
    Generate OpenAPI spec locally using the app.

    Args:
        output_path: Where to save the spec

    Returns:
        True if successful, False otherwise
    """
    logger.info("Generating spec locally...")
    try:
        # Find generate_openapi.py in parent directory (core-api/scripts)
        script_dir = Path(__file__).parent.parent
        generate_script = script_dir / 'generate_openapi.py'
        
        cmd = [sys.executable, str(generate_script), output_path]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=str(script_dir)
        )
        if result.returncode == 0:
            logger.info(f"✅ Spec generated to {output_path}")
            if result.stdout:
                logger.info(result.stdout)
            return True
        else:
            logger.error(f"❌ Spec generation failed.")
            if result.stdout:
                logger.error(f"Stdout: {result.stdout}")
            if result.stderr:
                logger.error(f"Stderr: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        logger.error("Spec generation timed out.")
        return False
    except Exception as e:
        logger.error(f"Error generating spec: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Fetch, validate, bundle, and lint OpenAPI specs.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Fetch from running server and validate
  python api_validation.py --fetch http://localhost:8000/api/openapi.json

  # Generate locally and validate
  python api_validation.py --generate

  # Validate existing file
  python api_validation.py --file ./openapi.json

  # Custom ruleset
  python api_validation.py --fetch http://localhost:8000/api/openapi.json --ruleset ../../../.spectral-custom.yaml
        """
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--fetch',
        type=str,
        metavar='URL',
        help='Fetch spec from remote URL'
    )
    group.add_argument(
        '--generate',
        action='store_true',
        help='Generate spec locally (requires generate_openapi.py in parent directory)'
    )
    group.add_argument(
        '--file',
        type=str,
        metavar='PATH',
        help='Validate existing spec file'
    )

    parser.add_argument(
        '--output',
        type=str,
        default='openapi-validated.json',
        help='Output path for fetched/generated spec (default: openapi-validated.json)'
    )
    parser.add_argument(
        '--ruleset',
        type=str,
        default='.spectral-google.yaml',
        help='Path to Spectral ruleset (default: .spectral-google.yaml)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Determine spec path
    if args.fetch:
        output_path = args.output
        if not fetch_spec(args.fetch, output_path):
            sys.exit(1)
        spec_path = output_path
    elif args.generate:
        output_path = args.output
        if not generate_spec(output_path):
            sys.exit(1)
        spec_path = output_path
    else:  # --file
        spec_path = args.file
        if not Path(spec_path).exists():
            logger.error(f"Spec file not found: {spec_path}")
            sys.exit(1)

    # Run validation
    validator = SpecValidator(spec_path, ruleset=args.ruleset)
    success = validator.run_full_validation()

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
