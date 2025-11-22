# Local SDK Development Guide

How to develop with a local SDK and easily switch between local and published versions.

---

## 🎯 **The Problem**

When you make API changes in `core-api/`, you need to:
1. Regenerate the SDK
2. Test the SDK changes in `web-app/`
3. But NOT commit the local SDK reference to git

**Solution:** Use `npm link` for seamless local development!

---

## 🚀 **Quick Start**

### **1. Generate the SDK Locally**

```powershell
# From project root
.\sdk\scripts\generate-sdk.ps1
```

This creates:
- `sdk/openapi.json` - OpenAPI spec
- `sdk/output/typescript/` - TypeScript SDK
- `sdk/output/python/` - Python SDK

---

### **2. Link the SDK for Local Development**

```bash
# Step 1: Create global link from SDK
cd sdk/output/typescript
npm link

# Step 2: Use the link in web-app
cd ../../../web-app
npm link @spearmint-finance/sdk
```

**What this does:**
- Creates a symlink: `web-app/node_modules/@spearmint-finance/sdk` → `sdk/output/typescript/`
- Changes to SDK are immediately available in web-app
- No need to modify `package.json`
- Easy to switch back to published version

---

### **3. Develop with Hot Reload**

Now you can make changes and see them immediately:

**Terminal 1 - Backend:**
```powershell
.\start_api.bat
```

**Terminal 2 - Frontend:**
```powershell
cd web-app
npm run dev
```

**Make changes:**
1. Edit API code in `core-api/src/`
2. Regenerate SDK: `.\sdk\scripts\generate-sdk.ps1`
3. Web-app automatically picks up changes! ✅

---

### **4. Switch Back to Published SDK**

When you're done developing:

```bash
cd web-app
npm unlink @spearmint-finance/sdk
npm install @spearmint-finance/sdk
```

This removes the symlink and installs the published version from npm.

---

## 📊 **Development Workflow**

### **Full Workflow Example:**

```powershell
# 1. Make API changes
code core-api/src/financial_analysis/api/routes/persons.py

# 2. Regenerate SDK
.\sdk\scripts\generate-sdk.ps1

# 3. Test in web-app (already linked)
cd web-app
npm run dev
# Open http://localhost:5173 and test

# 4. When satisfied, commit API changes
git add core-api/
git commit -m "Add new persons endpoint"
git push

# 5. CI/CD will automatically:
#    - Generate SDK
#    - Publish to npm
#    - Deploy to production

# 6. Later, update web-app to use published SDK
cd web-app
npm unlink @spearmint-finance/sdk
npm install @spearmint-finance/sdk@latest
```

---

## 🔄 **Switching Between Local and Published**

### **Use Local SDK:**

```bash
cd sdk/output/typescript && npm link
cd ../../../web-app && npm link @spearmint-finance/sdk
```

### **Use Published SDK:**

```bash
cd web-app
npm unlink @spearmint-finance/sdk
npm install @spearmint-finance/sdk
```

### **Check Which Version You're Using:**

```bash
cd web-app
npm ls @spearmint-finance/sdk
```

**Output if using local:**
```
@spearmint-finance/sdk@0.1.0 -> ./../sdk/output/typescript
```

**Output if using published:**
```
@spearmint-finance/sdk@0.1.0
```

---

## 🐳 **Using Local SDK in Docker Compose**

If you want to use the local SDK in Docker Compose (not recommended for daily dev):

### **Option 1: Volume Mount (Recommended)**

Update `docker-compose.yml`:

```yaml
web-app:
  volumes:
    - ./web-app/src:/app/src
    - ./sdk/output/typescript:/app/node_modules/@spearmint-finance/sdk
    - /app/node_modules
```

Then rebuild:
```bash
docker compose build web-app
docker compose up -d web-app
```

### **Option 2: File Path Reference**

Edit `web-app/package.json`:

```json
{
  "dependencies": {
    "@spearmint-finance/sdk": "file:../sdk/output/typescript"
  }
}
```

Then rebuild:
```bash
docker compose build web-app
docker compose up -d web-app
```

**⚠️ WARNING:** Don't commit this change! Use a `.gitignore` or remember to revert.

---

## 🎨 **Best Practices**

### **✅ DO:**

1. **Use `npm link` for local development** - Easiest and safest
2. **Regenerate SDK after API changes** - Keep them in sync
3. **Test locally before pushing** - Catch issues early
4. **Unlink before committing** - Use published SDK in production
5. **Document breaking changes** - Help other developers

### **❌ DON'T:**

1. **Don't commit local SDK references** - Use published versions
2. **Don't manually edit generated SDK** - Changes will be overwritten
3. **Don't skip SDK regeneration** - API and SDK will be out of sync
4. **Don't use file paths in package.json** - Easy to forget to revert

---

## 🔍 **Troubleshooting**

### **"SDK changes not reflecting"**

```bash
# Unlink and relink
cd web-app
npm unlink @spearmint-finance/sdk

cd ../sdk/output/typescript
npm link

cd ../../web-app
npm link @spearmint-finance/sdk

# Restart dev server
npm run dev
```

### **"Module not found: @spearmint-finance/sdk"**

You probably need to link it:
```bash
cd sdk/output/typescript && npm link
cd ../../../web-app && npm link @spearmint-finance/sdk
```

### **"Cannot find module 'typescript'"**

The SDK needs its dependencies installed:
```bash
cd sdk/output/typescript
npm install
npm link
```

### **"npm link not working in Docker"**

Use volume mounts or file path reference instead (see Docker section above).

---

## 📚 **Related Documentation**

- **SDK Generation:** `sdk/scripts/README.md`
- **Docker Hot Reload:** `DOCKER_HOT_RELOAD.md`
- **API Development:** `core-api/docs/`

---

## ✅ **Summary**

**For daily development:**
```bash
# One-time setup
.\sdk\scripts\generate-sdk.ps1
cd sdk/output/typescript && npm link
cd ../../web-app && npm link @spearmint-finance/sdk

# After API changes
.\sdk\scripts\generate-sdk.ps1
# Changes automatically available in web-app!

# Before committing
cd web-app
npm unlink @spearmint-finance/sdk
npm install @spearmint-finance/sdk
```

**This gives you:**
- ✅ Instant feedback on SDK changes
- ✅ No manual file copying
- ✅ Easy switching between local/published
- ✅ No risk of committing local references
- ✅ Same workflow as CI/CD

