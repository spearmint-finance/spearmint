# GitHub Actions Workflow: Create Postman Collection on Version Bump

This guide explains how to set up and use the GitHub Actions workflow that automatically creates a Postman collection whenever the API/SDK version is bumped.

## Overview

The workflow automatically creates a new Postman collection in your Spearmint workspace each time:
- The `package.json` version is updated (web-app or SDK)
- The `core-api/setup.py` version is updated
- The workflow is manually triggered
- The workflow file itself is updated

## Setup

### 1. Add GitHub Secrets

Add the following secrets to your GitHub repository:

**Settings → Secrets and variables → Actions**

| Secret Name | Description | Example |
|------------|-------------|---------|
| `POSTMAN_API_KEY` | Your Postman API key | `pmak_xxxxxxxxxxxxxxxxxxxx` |
| `POSTMAN_WORKSPACE_ID` | Your Spearmint Postman workspace ID | `20c3490b-76d5-4d25-8d3d-5f8a22d3ad39` |

#### How to get your Postman API Key:
1. Go to https://web.postman.co/settings/me/api-keys
2. Click "Generate API Key"
3. Copy the key and add it as `POSTMAN_API_KEY` secret

#### How to get your Workspace ID:
1. Open your Postman workspace
2. The workspace ID is in the URL: `https://app.postman.com/workspace/YOUR_WORKSPACE_ID/...`
3. Add it as `POSTMAN_WORKSPACE_ID` secret

### 2. Workflow File Location

The workflow is located at:
```
.github/workflows/create-postman-collection.yml
```

No additional setup needed—it will trigger automatically on version bumps.

## Usage

### Automatic Trigger

The workflow runs automatically when:
- Changes are pushed to `main` branch AND
- One of these files is modified:
  - `package.json` (web-app version)
  - `core-api/setup.py` (core-api version)
  - `sdk/package.json` (SDK version)

### Manual Trigger

To manually create a collection:

1. Go to **Actions** tab in your GitHub repository
2. Select **"Create Postman Collection on Version Bump"**
3. Click **"Run workflow"**
4. Enter the version number (e.g., `1.0.0`)
5. Click **"Run workflow"**

## Workflow Behavior

### When a version bump is detected:

1. **Extract Version**: Reads the version from `package.json`
2. **Create Collection**: Calls the Python script to create a Postman collection
3. **Upload Artifacts**: Saves collection info as GitHub artifact
4. **Comment on PR** (if applicable): Posts collection link in the pull request
5. **Report Results**: Displays success/failure in workflow logs

### Output

The workflow produces:
- A new Postman collection named `Spearmint API v{version}`
- Collection includes sample endpoints for:
  - Accounts (GET, LIST)
  - Users (GET, LIST, CREATE, UPDATE, DELETE)
  - Transactions (GET, LIST, CREATE)
- Pre-configured variables:
  - `baseUrl`: API base URL
  - `apiKey`: For authentication
- Pre-configured authentication using API key

## Collection Structure

Each generated collection includes:

```
Spearmint API v{version}/
├── Accounts
│   ├── Get Account
│   └── List Accounts
├── Users
│   ├── Get User
│   ├── List Users
│   ├── Create User
│   ├── Update User
│   └── Delete User
└── Transactions
    ├── Get Transaction
    ├── List Transactions
    └── Create Transaction
```

## GitHub Actions Outputs

The workflow sets the following outputs that can be used by subsequent steps:

```yaml
collection_id:   # The Postman collection ID
collection_name: # The collection name
collection_uid:  # The collection UID
```

Example usage in another workflow step:
```yaml
- name: Use collection ID
  run: echo "Collection created with ID: ${{ steps.create-collection.outputs.collection_id }}"
```

## Viewing Created Collections

After the workflow completes:

1. Check the workflow run logs for the collection link
2. Or access directly: `https://app.postman.com/workspace/{WORKSPACE_ID}/collections/{COLLECTION_ID}`
3. Or find it in your Postman workspace under the Collections tab

## Monitoring

### In GitHub:
1. Go to **Actions** tab
2. Click **"Create Postman Collection on Version Bump"**
3. View recent runs and their status

### In Postman:
1. Open your workspace
2. View the Collections tab
3. Filter by date or search for `Spearmint API v`

## Troubleshooting

### Workflow doesn't trigger

**Issue**: Workflow doesn't run on version bump
**Solution**:
- Verify secrets are set correctly
- Check that you're pushing to `main` branch
- Ensure the file being modified is in the trigger paths
- The version file must change (not just formatting)

### Collection creation fails

**Issue**: Workflow fails at "Create Postman collection" step
**Solution**:
- Verify `POSTMAN_API_KEY` is valid (regenerate if needed)
- Verify `POSTMAN_WORKSPACE_ID` is correct
- Check that your Postman account has permission to create collections
- Check workflow logs for detailed error messages

### Version not extracted

**Issue**: "Extracted version from web-app: (empty)"
**Solution**:
- Ensure `package.json` has a valid `version` field
- Check that JSON is properly formatted
- Verify the file path is correct

### PR comment not posting

**Issue**: Collection created but comment doesn't appear on PR
**Solution**:
- Only works on PRs merged to `main`
- Check GitHub token permissions (usually automatic with default token)
- Verify workflow has permission to write comments

## Customization

### Change Base URL

Edit `.github/workflows/create-postman-collection.yml`:

```yaml
- name: Create Postman collection
  run: |
    python dev-tools/collection_extractor/create_spearmint_collection.py \
      --workspace-id "${{ secrets.POSTMAN_WORKSPACE_ID }}" \
      --version "${{ steps.version.outputs.version }}" \
      --base-url "https://your-custom-url.com"  # Change this
```

### Add More Endpoints

Edit `dev-tools/collection_extractor/create_spearmint_collection.py`:

Find the `create_collection_payload()` function and add items to the collection structure:

```python
{
    "name": "Your New Endpoint",
    "request": {
        "method": "GET",
        "url": "{{baseUrl}}/your-endpoint",
        "header": [
            {
                "key": "Accept",
                "value": "application/json"
            }
        ]
    }
}
```

### Skip Collection Creation for Certain Commits

Add `[skip-collection]` to your commit message:

```bash
git commit -m "docs: update README [skip-collection]"
```

To implement this, modify the workflow file.

## Version Extraction Logic

The workflow extracts the version from:
1. `package.json` in the root (web-app)
2. Falls back to `core-api/setup.py` if package.json not found

To change this, edit the "Extract version" step in the workflow.

## Security Considerations

- **API Key**: Stored as a secret, never exposed in logs
- **Workspace ID**: Can be public (no sensitive data)
- **Workflow**: Only runs on `main` branch pushes
- **Artifacts**: Contains collection metadata, no credentials

## Related Files

- **Python Script**: `dev-tools/collection_extractor/create_spearmint_collection.py`
- **Workflow**: `.github/workflows/create-postman-collection.yml`
- **Collection Extractor Tool**: `dev-tools/collection_extractor/`

## Example Version Bump Workflow

Typical workflow when bumping version:

```bash
# 1. Update version in package.json
# 2. Commit and push
git add package.json
git commit -m "chore: bump version to 0.2.0"
git push

# 3. GitHub Actions automatically creates collection
# 4. Check workflow logs for collection link
# 5. Collection is available in your Postman workspace
```

## Next Steps

1. Set up the required secrets in GitHub
2. Create your first version bump to test the workflow
3. Monitor the workflow run in the Actions tab
4. Verify the collection appears in your Postman workspace
5. Customize endpoints as needed for your API

## Support

For issues with:
- **Postman API**: See [Postman API Documentation](https://learning.postman.com/docs/developer/postman-api/postman-api-overview/)
- **GitHub Actions**: See [GitHub Actions Documentation](https://docs.github.com/en/actions)
- **Python script**: Check `create_spearmint_collection.py` docstrings and comments
