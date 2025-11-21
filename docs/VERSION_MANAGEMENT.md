# Version Management Guide

## Overview

Spearmint uses a **single source of truth** for versioning: `version.json` at the project root.

All version numbers across the codebase are synchronized from this file.

## Current Version

Check the current version:
```bash
cat version.json
# Output: {"version": "0.0.1"}
```

## Versioning Strategy

### Semantic Versioning: `MAJOR.MINOR.PATCH`

- **PATCH** (`0.0.1` → `0.0.2`): Bug fixes, minor changes
- **MINOR** (`0.0.2` → `0.1.0`): New features, backwards-compatible
- **MAJOR** (`0.9.9` → `1.0.0`): Breaking changes, major milestones

### When Versions Get Bumped

Versions are **automatically bumped** when:
1. ✅ Tests pass
2. ✅ API Gateway builds successfully
3. ✅ SDK builds successfully

If any step fails → version does NOT bump (protection against bad releases)

## Files That Get Synchronized

When `version.json` changes, these files are automatically updated:

| File | Field | Example |
|------|-------|---------|
| `version.json` | `version` | `"version": "0.0.1"` |
| `web-app/package.json` | `version` | `"version": "0.0.1"` |
| `core-api/src/financial_analysis/__init__.py` | `__version__` | `__version__ = "0.0.1"` |
| `core-api/src/financial_analysis/api/openapi_config.py` | `API_VERSION` | `API_VERSION = "0.0.1"` |
| `core-api/src/financial_analysis/api/main.py` | Health endpoint | `"version": "0.0.1"` |

## Manual Version Bump (Local Development)

### Auto-increment patch version

```bash
# Bumps 0.0.1 → 0.0.2
python scripts/bump_version.py
```

### Set specific version

```bash
# Set to 0.1.0
python scripts/bump_version.py 0.1.0

# Set to 1.0.0
python scripts/bump_version.py 1.0.0
```

### What the script does

1. ✅ Updates `version.json`
2. ✅ Syncs to all files listed above
3. ✅ Shows you what changed
4. ℹ️ Does NOT commit or push (you do that manually)

### Example output

```bash
$ python scripts/bump_version.py

Current version: 0.0.1
New version: 0.0.2

  ✓ Updated version.json

Syncing version to files:
  ✓ Updated web-app/package.json
  ✓ Updated core-api/src/financial_analysis/__init__.py
  ✓ Updated core-api/src/financial_analysis/api/openapi_config.py
  ✓ Updated core-api/src/financial_analysis/api/main.py

✅ Version bumped: 0.0.1 → 0.0.2
✅ Updated 5 files

Next steps:
  1. Review changes: git diff
  2. Commit: git add . && git commit -m 'chore: bump version to 0.0.2'
  3. Tag: git tag v0.0.2
  4. Push: git push origin main --tags
```

## Automated Version Bump (CI/CD)

### GitHub Actions Workflow

File: `.github/workflows/deploy-and-version.yml`

**Trigger**: Push to `main` branch

**Flow**:
```
Push to main
  ↓
Run tests
  ↓
Build gateway (Docker)
  ↓
Build SDK (LibLab)
  ↓
✅ Both succeed → Bump version automatically
  ↓
Create git tag (v0.0.2)
  ↓
Create Postman collection with new version
  ↓
Done!
```

### What happens automatically

1. **Test** → Runs pytest
2. **Gateway** → Builds Docker image
3. **SDK** → Generates SDK via LibLab
4. **Version Bump** → Increments patch version
5. **Commit** → Commits version changes with `[skip ci]`
6. **Tag** → Creates git tag `v0.0.2`
7. **Postman** → Creates collection "Spearmint API v0.0.2"

### Monitoring the workflow

1. Go to GitHub → **Actions** tab
2. Select **"Deploy, Version Bump, and Postman Collection"**
3. View recent runs

### If something fails

- ❌ Tests fail → Stop (no version bump)
- ❌ Gateway fails → Stop (no version bump)
- ❌ SDK fails → Stop (no version bump)
- ✅ All pass → Version bumps automatically

## Checking Version Across Components

### From command line

```bash
# Root version (source of truth)
cat version.json

# Web app version
jq .version web-app/package.json

# Core API version
python -c "import sys; sys.path.insert(0, 'core-api/src'); from financial_analysis import __version__; print(__version__)"

# API health endpoint
curl http://localhost:8000/health | jq .version
```

### From API

```bash
GET /health
Response: {"status": "healthy", "version": "0.0.1"}
```

## Troubleshooting

### Versions are out of sync

**Problem**: Different files show different versions

**Solution**: Run the sync script
```bash
python scripts/bump_version.py 0.0.1  # Re-sync to current version
```

### Version didn't bump after successful deploy

**Problem**: Workflow completed but version is still 0.0.1

**Solution**: Check workflow logs
1. Go to GitHub → Actions
2. Check if `bump-version` job ran
3. Look for errors in the logs
4. Verify GitHub has write permissions (`permissions: contents: write`)

### Manual bump conflicts with automated bump

**Problem**: You bumped locally, workflow bumped automatically, merge conflict

**Solution**: 
1. Pull latest from main: `git pull origin main`
2. Check current version: `cat version.json`
3. If needed, bump again: `python scripts/bump_version.py X.X.X`
4. Commit and push

### Script says "file not found"

**Problem**: Script can't find a file to update

**Solution**: The file doesn't exist yet (e.g., CLI not set up)
- This is OK — the script skips it with a warning
- When the file is created, add it to `FILES_TO_UPDATE` in `scripts/bump_version.py`

## Best Practices

### ✅ DO

- Let CI/CD bump versions automatically after successful deploys
- Use semantic versioning (MAJOR.MINOR.PATCH)
- Commit version bumps with clear messages: `chore: bump version to X.X.X`
- Tag releases: `git tag vX.X.X`
- Document breaking changes when bumping MAJOR version

### ❌ DON'T

- Manually edit version numbers in multiple files (use the script!)
- Bump version without testing
- Skip version bumps for releases
- Use non-semantic versions (like "v1", "release-2")

## Git Tags

Every version bump creates a git tag:

```bash
# List all version tags
git tag -l "v*"

# Checkout a specific version
git checkout v0.0.1

# Create a release from a tag (on GitHub)
# Releases → Draft a new release → Choose tag
```

## Release Checklist

When creating a new release:

- [ ] All tests passing
- [ ] Gateway builds successfully
- [ ] SDK generates successfully
- [ ] Version bumped (automatically via CI/CD)
- [ ] Git tag created (automatically)
- [ ] Postman collection created (automatically)
- [ ] Release notes written (manual)
- [ ] Changelog updated (manual)

## FAQ

**Q: Can I manually bump without running CI/CD?**
A: Yes, use `python scripts/bump_version.py X.X.X` then commit and push.

**Q: What if I want to skip a version bump?**
A: Don't push to main, or add `[skip ci]` to your commit message (already done by the script).

**Q: How do I bump MAJOR or MINOR versions?**
A: Specify the version: `python scripts/bump_version.py 1.0.0` or `python scripts/bump_version.py 0.1.0`

**Q: Where is the version used?**
A: API responses, Postman collections, package distributions, git tags, documentation.

**Q: Can I have different versions for API vs SDK?**
A: Not currently. We use a single version for all components. If needed in the future, we can modify the strategy.

## Related Files

- `version.json` - Single source of truth
- `scripts/bump_version.py` - Version sync script
- `.github/workflows/deploy-and-version.yml` - Automated version bump workflow
- `.github/workflows/create-postman-collection.yml` - Postman collection creation
- `VERSIONING_STRATEGY.md` - Strategy document

---

**Current Version**: 0.0.1  
**Last Updated**: November 21, 2025
