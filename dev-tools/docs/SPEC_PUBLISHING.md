# Publishing OpenAPI Specs to Postman Spec Hub

This document explains how the Postman versioning system works and how it's integrated into the CI/CD pipeline.

## Overview

The Spearmint API uses an **update-in-place** versioning strategy for Postman assets. Instead of creating new specs and collections for each version, we maintain a single "current" spec and collection, using **forks for version history**.

### Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                     POSTMAN WORKSPACE                               │
│  ┌─────────────────────┐    ┌─────────────────────────────────┐    │
│  │ Spearmint API Spec  │ ──▶│ Spearmint API Collection        │    │
│  │ (always latest)     │    │ (always latest)                 │    │
│  │                     │    │                                 │    │
│  │ Updated in-place    │    │ Forks for version history:      │    │
│  │ each release        │    │  ├── v1.0.0 fork               │    │
│  │                     │    │  ├── v1.1.0 fork               │    │
│  │                     │    │  └── v1.2.0 fork               │    │
│  └─────────────────────┘    └─────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
                │
                │ Spec version history lives in Git
                ▼
┌─────────────────────────────────────────────────────────────────────┐
│  GIT REPOSITORY                                                     │
│  └── sdk/openapi.json                                              │
│      ├── v1.0.0 (git tag)                                          │
│      └── v1.1.0 (git tag)                                          │
│                                                                     │
│  To see previous spec: git show v1.0.0:sdk/openapi.json            │
└─────────────────────────────────────────────────────────────────────┘
```

### Version History Strategy

| Asset | Version History Via | Rationale |
|-------|---------------------|------------|
| OpenAPI Spec | **Git** (tags, commits) | Already versioned in repo; Postman doesn't support spec forking |
| Postman Collection | **Postman Forks** | Native forking support; preserves full collection state |

---

## Script Locations

```
dev-tools/postman/
├── common.py                        # Shared utilities
├── update_spec.py                   # Update spec content in-place
├── sync_collection.py               # Sync collection with spec
├── fork_collection.py               # Create version snapshot fork
└── update_collection_description.py # Update changelog in description

dev-tools/publish_spec.py            # Legacy: creates new spec (deprecated)
```

---

## How It Works (CI/CD Workflow)

When a new version is released, the following steps occur:

### Step 1: Fork Collection as Version Snapshot

Before updating, the current collection is forked with a version label (e.g., "v1.0.0 snapshot"). This preserves the previous version for reference.

```bash
python dev-tools/postman/fork_collection.py \
  --collection-id "$COLLECTION_ID" \
  --workspace-id "$WORKSPACE_ID" \
  --version "1.0.0"
```

### Step 2: Update Spec Content In-Place

The spec file content is updated in Postman Spec Hub without creating a new spec entity.

```bash
python dev-tools/postman/update_spec.py \
  --spec-id "$SPEC_ID" \
  --spec-file "sdk/openapi.json" \
  --version "1.1.0"
```

### Step 3: Sync Collection with Updated Spec

The collection is regenerated from the updated spec to reflect API changes.

```bash
python dev-tools/postman/sync_collection.py \
  --spec-id "$SPEC_ID" \
  --collection-uid "$COLLECTION_UID"
```

### Step 4: Update Collection Description

The collection description is updated with version changelog and links to historical forks.

```bash
python dev-tools/postman/update_collection_description.py \
  --collection-id "$COLLECTION_ID" \
  --version "1.1.0"
```

---

## CI/CD Integration

The workflow is integrated into `.github/workflows/deploy-and-version.yml` as the `publish-spec-and-collection` job.

### Workflow Steps

1. **Fork collection** - Archives the current collection state with version label
2. **Update spec** - Replaces spec content in Postman Spec Hub
3. **Sync collection** - Regenerates collection from updated spec
4. **Update description** - Adds version changelog to collection

### When It Runs

The `publish-spec-and-collection` job runs:

- ✅ After the version is bumped
- ✅ Only when the version actually changed
- ✅ In parallel with `publish-sdk`

---

## Required Secrets

Add these secrets to your GitHub repository:

| Secret Name | Description | How to Get |
|-------------|-------------|------------|
| `POSTMAN_API_KEY` | Postman API key | [Generate in Postman Settings](https://go.postman.co/settings/me/api-keys) |
| `POSTMAN_WORKSPACE_ID` | Main workspace ID | Found in workspace URL after `~` |
| `POSTMAN_SPEC_ID` | ID of the main spec | From spec URL (see below) |
| `POSTMAN_COLLECTION_UID` | UID of the main collection | From collection URL (see below) |
| `POSTMAN_ARCHIVE_WORKSPACE_ID` | Archive workspace for version forks | Create new workspace, get ID from URL |

---

## One-Time Setup

Before the workflow can run, you need to get the IDs of your existing spec and collection from Postman.

### 1. Get the Spec ID

- Open your Postman workspace
- Go to the Spec Hub and find your latest spec (e.g., "Spearmint Finance API - v1.0.0")
- The spec ID is in the URL: `https://app.postman.com/workspace/.../specs/{SPEC_ID}`

### 2. Get the Collection UID

- Open your collection (e.g., "spearmint-api-prod")
- The collection UID is in the URL: `https://app.postman.com/workspace/.../collection/{COLLECTION_UID}`

### 3. Create an Archive Workspace

- In Postman, create a new workspace (e.g., "Spearmint Archive")
- The workspace ID is in the URL after the `~`: `https://app.postman.com/workspace/Name~{WORKSPACE_ID}`

### 4. Add Secrets to GitHub

Go to: Repository → Settings → Secrets and variables → Actions → New repository secret

Add:

- `POSTMAN_SPEC_ID` = (spec ID from step 1)
- `POSTMAN_COLLECTION_UID` = (collection UID from step 2)
- `POSTMAN_ARCHIVE_WORKSPACE_ID` = (archive workspace ID from step 3)

> **Note**: If you're starting fresh with no existing assets, you can use `dev-tools/publish_spec.py` to create the initial spec and collection, then extract the IDs from its output.

---

## Viewing Version History

### Spec History (via Git)

```bash
# List all version tags
git tag -l "v*"

# View spec at a specific version
git show v1.0.0:sdk/openapi.json

# Compare specs between versions
git diff v1.0.0:sdk/openapi.json v1.1.0:sdk/openapi.json
```

### Collection History (via Postman Forks)

1. Open the main collection in Postman
2. Click on the collection name
3. Select "Forks" tab
4. Each fork is labeled with version (e.g., "v1.0.0 snapshot")

---

## Output

### Console Output (Update Flow)

```text
Creating collection fork (version snapshot)...
  Collection ID: 12345678-abcd-1234-efgh-567890abcdef
  Workspace ID: 1f0df51a-8658-4ee8-a2a1-d2567dfa09a9
  Fork label: v1.0.0 snapshot

✓ Fork created successfully!

Updating OpenAPI spec in Postman Spec Hub...
  Spec ID: b4fc1bdc-6587-4f9b-95c9-f768146089b4
  Spec file: sdk/openapi.json
  Version: 1.1.0

✓ Spec file updated successfully!

Syncing collection with spec...
  Spec ID: b4fc1bdc-6587-4f9b-95c9-f768146089b4
  Collection UID: 12345678-abcd-1234-efgh-567890abcdef

✓ Collection synced successfully!
```

---

## Error Handling

The scripts handle common errors with retry logic for transient failures:

- **File Not Found**: `ERROR: Spec file not found: sdk/openapi.json`
- **Invalid JSON**: `ERROR: Invalid JSON in spec file: ...`
- **API Errors**: `ERROR: Postman API error (HTTP 400): {...}`
- **Network Errors**: Automatically retried with exponential backoff

---

## Related Documentation

- [GitHub Issue #14: Versioning Strategy](https://github.com/spearmint-finance/spearmint/issues/14)
- [Postman API Collection Creation](./POSTMAN_API_COLLECTION_CREATION.md)
- [Postman API Documentation](https://www.postman.com/postman/workspace/postman-public-workspace/documentation/12959542-c8142d51-e97c-46b6-bd77-52bb66712c9a)
- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
