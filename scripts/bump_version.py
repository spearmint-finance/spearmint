#!/usr/bin/env python3
"""
Version Bump Script

Updates version.json and syncs the version to all relevant files across the project.

Usage:
    python bump_version.py           # Auto-increment patch version
    python bump_version.py 0.1.0     # Set specific version
    python bump_version.py --help    # Show help
"""

import json
import sys
import re
from pathlib import Path
from typing import List, Tuple


# Root directory (parent of scripts/)
ROOT_DIR = Path(__file__).parent.parent

# Source of truth
VERSION_FILE = ROOT_DIR / "version.json"

# Files to sync version to
FILES_TO_UPDATE = [
    (ROOT_DIR / "web-app" / "package.json", "json_version"),
    (ROOT_DIR / "core-api" / "src" / "financial_analysis" / "__init__.py", "python_version"),
    (ROOT_DIR / "core-api" / "src" / "financial_analysis" / "api" / "openapi_config.py", "python_api_version"),
    (ROOT_DIR / "core-api" / "src" / "financial_analysis" / "api" / "main.py", "python_health_version"),
]


def read_version() -> str:
    """Read current version from version.json."""
    if not VERSION_FILE.exists():
        print(f"Error: {VERSION_FILE} not found!")
        sys.exit(1)
    
    with open(VERSION_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    return data["version"]


def bump_patch(version: str) -> str:
    """Increment patch version (e.g., 0.0.1 -> 0.0.2)."""
    try:
        major, minor, patch = map(int, version.split('.'))
        patch += 1
        return f"{major}.{minor}.{patch}"
    except (ValueError, AttributeError):
        print(f"Error: Invalid version format '{version}'. Expected MAJOR.MINOR.PATCH")
        sys.exit(1)


def validate_version(version: str) -> bool:
    """Validate version format (semantic versioning)."""
    pattern = r'^\d+\.\d+\.\d+$'
    return bool(re.match(pattern, version))


def update_version_json(new_version: str) -> None:
    """Update version.json with new version."""
    with open(VERSION_FILE, "w", encoding="utf-8") as f:
        json.dump({"version": new_version}, f, indent=2)
        f.write("\n")  # Add trailing newline


def update_json_version(filepath: Path, new_version: str) -> None:
    """Update version in a JSON file (e.g., package.json)."""
    if not filepath.exists():
        print(f"Warning: {filepath} not found, skipping")
        return
    
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    data["version"] = new_version
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")  # Add trailing newline


def update_python_version(filepath: Path, new_version: str) -> None:
    """Update __version__ = "x.x.x" in Python files."""
    if not filepath.exists():
        print(f"Warning: {filepath} not found, skipping")
        return
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Replace __version__ = "x.x.x"
    updated_content = re.sub(
        r'__version__\s*=\s*["\'][\d.]+["\']',
        f'__version__ = "{new_version}"',
        content
    )
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(updated_content)


def update_python_api_version(filepath: Path, new_version: str) -> None:
    """Update API_VERSION = "x.x.x" in Python files."""
    if not filepath.exists():
        print(f"Warning: {filepath} not found, skipping")
        return
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Replace API_VERSION = "x.x.x"
    updated_content = re.sub(
        r'API_VERSION\s*=\s*["\'][\d.]+["\']',
        f'API_VERSION = "{new_version}"',
        content
    )
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(updated_content)


def update_python_health_version(filepath: Path, new_version: str) -> None:
    """Update health check endpoint version in main.py."""
    if not filepath.exists():
        print(f"Warning: {filepath} not found, skipping")
        return
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Replace {"status": "healthy", "version": "x.x.x"}
    updated_content = re.sub(
        r'"version":\s*["\'][\d.]+["\']',
        f'"version": "{new_version}"',
        content
    )
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(updated_content)


def sync_version_to_files(new_version: str) -> List[Path]:
    """Sync version to all configured files."""
    updated_files = [VERSION_FILE]
    
    for filepath, file_type in FILES_TO_UPDATE:
        try:
            if file_type == "json_version":
                update_json_version(filepath, new_version)
            elif file_type == "python_version":
                update_python_version(filepath, new_version)
            elif file_type == "python_api_version":
                update_python_api_version(filepath, new_version)
            elif file_type == "python_health_version":
                update_python_health_version(filepath, new_version)
            
            if filepath.exists():
                updated_files.append(filepath)
                print(f"  ✓ Updated {filepath.relative_to(ROOT_DIR)}")
        except Exception as e:
            print(f"  ✗ Error updating {filepath}: {e}")
    
    return updated_files


def show_help():
    """Display help message."""
    print(__doc__)
    print("\nCurrent version:", read_version())
    print("\nFiles that will be updated:")
    for filepath, _ in FILES_TO_UPDATE:
        exists = "✓" if filepath.exists() else "✗"
        print(f"  {exists} {filepath.relative_to(ROOT_DIR)}")


def main():
    """Main entry point."""
    # Handle help
    if len(sys.argv) > 1 and sys.argv[1] in ["--help", "-h", "help"]:
        show_help()
        sys.exit(0)
    
    # Read current version
    current_version = read_version()
    print(f"Current version: {current_version}")
    
    # Determine new version
    if len(sys.argv) > 1:
        new_version = sys.argv[1]
        if not validate_version(new_version):
            print(f"Error: Invalid version format '{new_version}'")
            print("Expected format: MAJOR.MINOR.PATCH (e.g., 0.1.0)")
            sys.exit(1)
    else:
        # Auto-bump patch version
        new_version = bump_patch(current_version)
    
    print(f"New version: {new_version}")
    print()
    
    # Update version.json
    update_version_json(new_version)
    print(f"  ✓ Updated {VERSION_FILE.relative_to(ROOT_DIR)}")
    
    # Sync to all files
    print("\nSyncing version to files:")
    updated_files = sync_version_to_files(new_version)
    
    print()
    print(f"✅ Version bumped: {current_version} → {new_version}")
    print(f"✅ Updated {len(updated_files)} files")
    print()
    print("Next steps:")
    print("  1. Review changes: git diff")
    print("  2. Commit: git add . && git commit -m 'chore: bump version to {}'".format(new_version))
    print("  3. Tag: git tag v{}".format(new_version))
    print("  4. Push: git push origin main --tags")


if __name__ == "__main__":
    main()
