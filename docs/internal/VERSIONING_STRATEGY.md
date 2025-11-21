# Versioning Strategy for Spearmint

## Current State

**Problem**: Versions scattered across multiple files with inconsistencies
- `web-app/package.json`: 1.0.0
- `core-api/src/financial_analysis/__init__.py`: 0.1.0
- `core-api/src/financial_analysis/api/openapi_config.py`: 1.0.0
- `core-api/src/financial_analysis/api/main.py`: 1.0.0 (hardcoded)
- SDK, CLI: no version tracking

## Proposed Solution: Single Source of Truth

### Option 1: Centralized version.json (Recommended)
```
Root: version.json → {"version": "0.0.1"}
```

**Pros:**
- Single file to update
- Easy to read and parse
- Works across all components
- Language-agnostic
- Easy for scripts/CI-CD

**Cons:**
- Requires synchronization to update package.json

**Workflow:**
```
1. Update version.json only (0.0.1 → 0.0.2)
2. Script/CI syncs to:
   - web-app/package.json
   - core-api/__init__.py
   - core-api/openapi_config.py
   - cli/setup.py (when we have it)
   - sdk/package.json (when we have it)
3. All tests, docs, collections use version from version.json
```

### Option 2: package.json as Source (Alternative)
```
Root: package.json → {"version": "0.0.1"}
```

**Pros:**
- Standard for Node projects
- Works with npm tools

**Cons:**
- Less intuitive for Python components
- Need Python script to read and sync
- Package.json is usually app-specific, not for shared versions

### Option 3: Hybrid Approach (Most Flexible)
```
Each component has its own version, but sync'd from root config
- version.json (source)
- web-app/package.json (synced)
- core-api/setup.py (synced, create if needed)
- cli/setup.py (synced, create if needed)
- sdk/package.json (synced, when needed)
```

---

## What Gets Updated When Version Changes

### Files to Sync
1. ✅ `version.json` (master source)
2. ✅ `web-app/package.json` 
3. ✅ `core-api/src/financial_analysis/__init__.py`
4. ✅ `core-api/src/financial_analysis/api/openapi_config.py`
5. ✅ `core-api/src/financial_analysis/api/main.py` (health endpoint)
6. ⏳ `cli/setup.py` (create when CLI is packaged)
7. ⏳ `sdk/package.json` (create when SDK is published)

### Where Version is Read
- **GitHub Actions**: Read from `version.json`
- **Postman Collections**: Use version from GH Actions
- **API Docs**: Use `openapi_config.py`
- **Package Distributions**: Use respective package.json/setup.py

---

## Versioning Scheme: Semantic Versioning

`MAJOR.MINOR.PATCH` → `0.0.1`

- `0` = MAJOR (pre-release, breaking changes expected)
- `0` = MINOR (features, enhancements)
- `1` = PATCH (bug fixes)

**When to increment:**
- `0.0.1` → `0.0.2`: Bug fixes
- `0.0.1` → `0.1.0`: New features
- `0.1.0` → `1.0.0`: Production-ready

---

## Implementation Plan

### Phase 1: Setup (Today)
1. Create `version.json` with `0.0.1`
2. Update all version references to match
3. Create sync script (optional now, needed for automation)

### Phase 2: GitHub Actions (Next)
1. Update workflow to read from `version.json`
2. Extract version in workflow
3. Create Postman collections with correct version

### Phase 3: Automation (Future)
1. Create `bump-version.sh` script to:
   - Prompt for new version
   - Update `version.json`
   - Sync to all component files
   - Create git tag
   - Trigger GitHub Actions
2. Or use GitHub Actions + semantic versioning tools

---

## Questions for You

1. **Which approach?**
   - Option 1: Centralized `version.json`
   - Option 2: `package.json` as source
   - Option 3: Hybrid

2. **Sync method?**
   - Manual (edit version.json, then manually sync)
   - Script (create bash/Python script to auto-sync)
   - GitHub Actions (auto-sync on push)

3. **Versioning scope?**
   - Single version for all (API + SDK + CLI + Web)
   - Separate versions per component (more complex)

4. **Starting version?**
   - `0.0.1` (current proposal)
   - Something else?

---

## ✅ IMPLEMENTED: Option 1 (Centralized) with Automated Sync

**Status**: Complete and deployed

**What was built:**

1. ✅ **version.json** - Single source of truth at project root
2. ✅ **scripts/bump_version.py** - Python script to sync versions across all files
3. ✅ **GitHub Actions Workflow** - Automated version bump after successful deployments
4. ✅ **All files synced** - Updated to version 0.0.1

**How it works:**

```
Push to main → Tests → Gateway Build → SDK Build
                                          ↓
                                    Both succeed?
                                          ↓
                                    Bump version (0.0.1 → 0.0.2)
                                          ↓
                                    Sync all files
                                          ↓
                                    Create git tag (v0.0.2)
                                          ↓
                                    Create Postman collection
```

**Files Created:**
- `version.json` - Single source of truth
- `scripts/bump_version.py` - Version sync script (230 lines)
- `.github/workflows/deploy-and-version.yml` - Main workflow
- `docs/VERSION_MANAGEMENT.md` - Complete documentation

**Files Updated:**
- `.github/workflows/create-postman-collection.yml` - Now reads from version.json
- All version references set to 0.0.1

**See**: `docs/VERSION_MANAGEMENT.md` for complete usage guide
