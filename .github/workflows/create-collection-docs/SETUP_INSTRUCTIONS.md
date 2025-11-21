# Quick Setup: Postman Collection Auto-Creation

## 5-Minute Setup

### Step 1: Get Your Secrets

1. **Postman API Key**
   - Visit: https://web.postman.co/settings/me/api-keys
   - Click "Generate API Key"
   - Copy the key (save it temporarily)

2. **Workspace ID**
   - Open your Postman workspace
   - Copy the ID from the URL: `https://app.postman.com/workspace/{WORKSPACE_ID}/...`

### Step 2: Add Secrets to GitHub

1. Go to your GitHub repo → **Settings** → **Secrets and variables** → **Actions**
2. Click **"New repository secret"**
3. Add `POSTMAN_API_KEY` with your API key
4. Click **"New repository secret"** again
5. Add `POSTMAN_WORKSPACE_ID` with your workspace ID

### Step 3: Verify Setup

The workflow will now automatically:
- Create a collection when you bump the version in `package.json`
- Create a collection when you bump the version in `core-api/setup.py`
- Can be manually triggered from Actions tab

## Test It

To test the setup:

```bash
# 1. Edit package.json and change version (e.g., 0.1.0 → 0.1.1)
# 2. Commit and push
git add package.json
git commit -m "chore: bump version"
git push

# 3. Go to GitHub → Actions tab
# 4. Watch the workflow run
# 5. Check your Postman workspace for new collection
```

## Manual Trigger

Don't want to bump version? Manually trigger:

1. GitHub → **Actions** tab
2. Select **"Create Postman Collection on Version Bump"**
3. Click **"Run workflow"**
4. Enter version number
5. Click **"Run workflow"**

## Files Created

- **Workflow**: `.github/workflows/create-postman-collection.yml`
- **Python Script**: `dev-tools/collection_extractor/create_spearmint_collection.py`
- **Guide**: `create-collection-docs/CREATE_POSTMAN_COLLECTION_GUIDE.md`

## What Gets Created

Each collection includes:

```
Spearmint API v{version}
├── Accounts (GET, LIST)
├── Users (GET, LIST, CREATE, UPDATE, DELETE)
└── Transactions (GET, LIST, CREATE)
```

With pre-configured:
- Variables for `baseUrl` and `apiKey`
- API key authentication
- Sample request bodies

## Troubleshooting

**Workflow doesn't run?**
- Verify secrets are set (Settings → Secrets and variables → Actions)
- Make sure you're pushing to `main` branch
- Check that you're modifying one of the trigger files

**Collection not created?**
- Check workflow logs in Actions tab for error message
- Verify API key is valid (regenerate if needed)
- Verify workspace ID is correct

**Need to customize?**
- Edit `dev-tools/collection_extractor/create_spearmint_collection.py` to add/remove endpoints
- Edit `.github/workflows/create-postman-collection.yml` to change base URL or version extraction logic

## Need Help?

See full guide: `CREATE_POSTMAN_COLLECTION_GUIDE.md`
