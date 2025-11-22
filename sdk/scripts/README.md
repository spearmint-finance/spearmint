# SDK Generation Scripts

Scripts for generating the Spearmint SDK locally using LibLab.

---

## 📋 **Prerequisites**

### 1. Install LibLab CLI

```bash
npm install -g liblab
```

### 2. Get LibLab Token

1. Sign up at https://liblab.com
2. Get your API token from the dashboard
3. Set the environment variable:

**Windows (PowerShell):**
```powershell
$env:LIBLAB_TOKEN = "your-token-here"
```

**Linux/macOS:**
```bash
export LIBLAB_TOKEN="your-token-here"
```

### 3. Activate Python Virtual Environment

```bash
# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate
```

---

## 🚀 **Usage**

### **Windows (PowerShell)**

```powershell
# Generate OpenAPI spec + SDK
.\sdk\scripts\generate-sdk.ps1

# Only generate SDK (skip spec generation)
.\sdk\scripts\generate-sdk.ps1 -SkipSpec

# Show help
.\sdk\scripts\generate-sdk.ps1 -Help
```

### **Linux/macOS (Bash)**

```bash
# Make script executable (first time only)
chmod +x sdk/scripts/generate-sdk.sh

# Generate OpenAPI spec + SDK
./sdk/scripts/generate-sdk.sh

# Only generate SDK (skip spec generation)
./sdk/scripts/generate-sdk.sh --skip-spec

# Show help
./sdk/scripts/generate-sdk.sh --help
```

---

## 📂 **What Gets Generated**

After running the script, you'll find:

```
sdk/
├── openapi.json              # Generated OpenAPI spec
└── output/
    ├── typescript/           # TypeScript SDK
    │   ├── src/
    │   ├── package.json
    │   └── ...
    └── python/               # Python SDK
        ├── src/
        ├── setup.py
        └── ...
```

---

## 🔄 **Development Workflow**

### **After Making API Changes:**

1. **Make changes** to your FastAPI code in `core-api/src/`

2. **Generate the SDK:**
   ```powershell
   .\sdk\scripts\generate-sdk.ps1
   ```

3. **Link the SDK locally** (first time only):
   ```bash
   cd sdk/output/typescript
   npm link
   
   cd ../../../web-app
   npm link @spearmint-finance/sdk
   ```

4. **Test your changes** in the web app - it now uses the local SDK!

5. **When ready to publish:**
   - Push your changes to GitHub
   - The CI/CD workflow will automatically publish the SDK to npm

---

## 🔗 **Using Local SDK in Development**

### **Option 1: npm link (Recommended)**

This creates a symlink so changes to the SDK are immediately available:

```bash
# In SDK directory
cd sdk/output/typescript
npm link

# In web-app directory
cd ../../../web-app
npm link @spearmint-finance/sdk
```

**Benefits:**
- ✅ Changes to SDK are immediately available
- ✅ No need to rebuild web-app
- ✅ Easy to switch back to published version

**To unlink:**
```bash
cd web-app
npm unlink @spearmint-finance/sdk
npm install @spearmint-finance/sdk
```

---

### **Option 2: File Path Reference**

Edit `web-app/package.json`:

```json
{
  "dependencies": {
    "@spearmint-finance/sdk": "file:../sdk/output/typescript"
  }
}
```

Then run:
```bash
cd web-app
npm install
```

**Benefits:**
- ✅ Works in Docker Compose
- ✅ Explicit in package.json

**Drawbacks:**
- ❌ Need to run `npm install` after SDK changes
- ❌ Easy to forget to change back before committing

---

## 🐳 **Using Local SDK in Docker Compose**

If you want to use the local SDK in Docker Compose:

1. **Generate the SDK:**
   ```powershell
   .\sdk\scripts\generate-sdk.ps1
   ```

2. **Update `web-app/package.json`:**
   ```json
   {
     "dependencies": {
       "@spearmint-finance/sdk": "file:../sdk/output/typescript"
     }
   }
   ```

3. **Rebuild the web-app container:**
   ```bash
   docker compose build web-app
   docker compose up -d web-app
   ```

---

## 🔍 **Troubleshooting**

### **"LibLab CLI not found"**

Install it:
```bash
npm install -g liblab
```

### **"LIBLAB_TOKEN not set"**

Set the environment variable:
```powershell
# Windows
$env:LIBLAB_TOKEN = "your-token"

# Linux/macOS
export LIBLAB_TOKEN="your-token"
```

### **"Virtual environment not found"**

Activate your Python virtual environment:
```bash
# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate
```

### **"OpenAPI generation failed"**

Make sure you're in the project root and dependencies are installed:
```bash
cd core-api
pip install -r requirements.txt
pip install -e .
```

### **SDK changes not reflecting in web-app**

If using npm link:
```bash
# Unlink and relink
cd web-app
npm unlink @spearmint-finance/sdk
cd ../sdk/output/typescript
npm link
cd ../../../web-app
npm link @spearmint-finance/sdk
```

---

## 📊 **Script Process**

The script follows the same process as the CI/CD workflow:

1. **Generate OpenAPI Spec** (unless `--skip-spec`)
   - Installs Python dependencies
   - Runs `core-api/scripts/generate_openapi.py`
   - Outputs to `sdk/openapi.json`

2. **Build SDK with LibLab**
   - Updates `liblab.config.json` to use local spec
   - Runs `liblab build`
   - Outputs to `sdk/output/typescript/` and `sdk/output/python/`

---

## 🎯 **Quick Reference**

```bash
# Full generation (spec + SDK)
.\sdk\scripts\generate-sdk.ps1

# Only SDK (use existing spec)
.\sdk\scripts\generate-sdk.ps1 -SkipSpec

# Link SDK for local development
cd sdk/output/typescript && npm link
cd ../../../web-app && npm link @spearmint-finance/sdk

# Unlink SDK (use published version)
cd web-app && npm unlink @spearmint-finance/sdk && npm install
```

