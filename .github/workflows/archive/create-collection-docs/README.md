# Postman Collection Auto-Creation System

Complete implementation for automatically creating Postman collections when Spearmint API/SDK versions are bumped.

## What Was Created

### 1. Python Script
**File**: `dev-tools/collection_extractor/create_spearmint_collection.py`

A production-ready Python script that:
- Creates Postman collections via the Postman API
- No external dependencies (uses standard library only)
- Supports CLI arguments for flexibility
- Works in GitHub Actions and locally
- Saves collection details to JSON
- Sets GitHub Actions outputs for CI/CD integration

**Usage**:
```bash
python create_spearmint_collection.py \
  --workspace-id YOUR_WORKSPACE_ID \
  --version 1.0.0 \
  --base-url https://api.spearmint.ai
```

### 2. GitHub Actions Workflow
**File**: `.github/workflows/create-postman-collection.yml`

Automatically triggers when:
- `package.json` is modified (version bump)
- `core-api/setup.py` is modified (version bump)
- Workflow is manually triggered

Workflow performs:
1. Extract version from package.json
2. Create collection in Postman workspace
3. Comment on PR with collection link (if applicable)
4. Upload collection info as artifact
5. Report results

### 3. Documentation
- **SETUP_INSTRUCTIONS.md**: Quick 5-minute setup guide
- **CREATE_POSTMAN_COLLECTION_GUIDE.md**: Comprehensive reference guide

## Quick Start

### Prerequisites
- GitHub repository access (to set secrets)
- Postman API key (get from https://web.postman.co/settings/me/api-keys)
- Postman workspace ID

### 3-Step Setup

1. **Add GitHub Secrets**
   ```
   Settings → Secrets and variables → Actions
   - POSTMAN_API_KEY: your_api_key
   - POSTMAN_WORKSPACE_ID: your_workspace_id
   ```

2. **Test Locally** (optional)
   ```bash
   export POSTMAN_API_KEY=your_key
   python dev-tools/collection_extractor/create_spearmint_collection.py \
     --workspace-id your_workspace_id \
     --version 0.1.0
   ```

3. **Deploy**
   - Push to main branch
   - Or manually trigger from Actions tab
   - Workflow creates collection automatically

## Collection Structure

Each generated collection includes:

```
Spearmint API v{version}
├── Variables
│   ├── baseUrl (https://api.spearmint.ai)
│   └── apiKey (for authentication)
├── Auth
│   └── API Key authentication
├── Accounts
│   ├── GET /accounts
│   └── GET /accounts/:accountId
├── Users
│   ├── GET /users
│   ├── GET /users/:userId
│   ├── POST /users (with sample body)
│   ├── PUT /users/:userId (with sample body)
│   └── DELETE /users/:userId
└── Transactions
    ├── GET /transactions
    ├── GET /transactions/:transactionId
    └── POST /transactions (with sample body)
```

## Key Features

✅ **Zero Dependencies**: Uses only Python standard library
✅ **GitHub Actions Ready**: Integrates seamlessly with workflows
✅ **Error Handling**: Clear error messages and HTTP status reporting
✅ **Flexible**: CLI arguments for version, base URL, workspace
✅ **Tracked**: Saves collection info to JSON and GitHub artifacts
✅ **Automated**: Triggers on version bumps automatically
✅ **PR Integration**: Comments on PRs with collection link
✅ **Secure**: API key stored as GitHub secret

## Automation Workflow

### When you bump the version:

```
1. Edit package.json (version change)
   ↓
2. Commit and push to main
   ↓
3. GitHub Actions detects version change
   ↓
4. Workflow runs create_spearmint_collection.py
   ↓
5. Collection created in Postman workspace
   ↓
6. PR comment posted (if applicable)
   ↓
7. Collection info saved as artifact
```

## File Locations

```
spearmint/
├── .github/workflows/
│   ├── create-postman-collection.yml          # The workflow
│   └── create-collection-docs/
│       ├── README.md                          # This file
│       ├── SETUP_INSTRUCTIONS.md              # Quick setup guide
│       └── CREATE_POSTMAN_COLLECTION_GUIDE.md # Full reference
├── dev-tools/collection_extractor/
│   ├── create_spearmint_collection.py         # Python script
│   ├── extract_collection.ps1                 # PowerShell tool (bonus)
│   ├── analyze_collection.py                  # Analysis tool (bonus)
│   ├── README.md                              # Tool documentation
│   └── POSTMAN_API_COLLECTION_CREATION.md     # API reference
```

## Customization

### Add More Endpoints

Edit `create_spearmint_collection.py`:

```python
# In create_collection_payload() function
{
    "name": "My New Endpoint",
    "request": {
        "method": "POST",
        "url": "{{baseUrl}}/my-endpoint",
        "body": {
            "mode": "raw",
            "raw": json.dumps({"field": "value"}, indent=2)
        }
    }
}
```

### Change Base URL

Edit workflow `.github/workflows/create-postman-collection.yml`:

```yaml
--base-url "https://your-custom-api.com"
```

### Change Trigger Conditions

Edit workflow `on:` section to trigger on different events:

```yaml
on:
  push:
    branches: [main]
    paths:
      - 'your-file.json'
      - 'your-version-file.txt'
```

## GitHub Actions Outputs

The workflow sets outputs for use in subsequent steps:

```
collection_id   - The Postman collection ID
collection_name - The collection name
collection_uid  - The collection UID
```

Use in other workflows:
```yaml
- name: Use collection
  run: echo "ID: ${{ steps.create-collection.outputs.collection_id }}"
```

## Testing

### Local Test
```bash
export POSTMAN_API_KEY=your_key
python create_spearmint_collection.py \
  --workspace-id 20c3490b-76d5-4d25-8d3d-5f8a22d3ad39 \
  --version test-1.0.0
```

### Workflow Test
1. Go to GitHub Actions tab
2. Select "Create Postman Collection on Version Bump"
3. Click "Run workflow"
4. Enter test version (e.g., test-1.0.0)
5. Check workspace for new collection

### Verify Success
1. Check GitHub Actions logs for collection link
2. Or find in Postman workspace → Collections tab
3. Verify endpoints are present

## Security

- **API Key**: Stored in GitHub Secrets, never logged
- **Workspace ID**: Can be public (no sensitive data)
- **Workflow**: Only runs on authenticated pushes to main
- **Artifacts**: Collection metadata only, no credentials

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Workflow doesn't run | Verify secrets are set; check file modification paths |
| Collection not created | Check API key validity; verify workspace ID |
| Version not detected | Ensure package.json has valid version field |
| PR comment missing | Only works on PRs; check GitHub permissions |
| Network error | Check Postman API availability and rate limits |

## Related Tools

Also included in this toolset:

- **extract_collection.ps1**: PowerShell script to download any Postman collection
- **analyze_collection.py**: Python script to analyze and report on collections
- **POSTMAN_API_COLLECTION_CREATION.md**: Full Postman API reference

## Next Steps

1. ✅ Review `create-collection-docs/SETUP_INSTRUCTIONS.md`
2. ✅ Add GitHub Secrets
3. ✅ Test with manual workflow trigger
4. ✅ Bump a version to test automation
5. ✅ Customize endpoints as needed

## Support

- **Setup Help**: `create-collection-docs/SETUP_INSTRUCTIONS.md`
- **Full Guide**: `create-collection-docs/CREATE_POSTMAN_COLLECTION_GUIDE.md`
- **API Reference**: `dev-tools/collection_extractor/POSTMAN_API_COLLECTION_CREATION.md`
- **Script Help**: `python create_spearmint_collection.py --help`

---

**Status**: ✅ Ready for production
**Last Updated**: November 21, 2025
**Tested**: Yes - successfully created collections in Postman workspace
