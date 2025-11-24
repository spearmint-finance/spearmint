# ✅ Workflow Restructured - Validate First, Then Deploy!

## 🎯 New Workflow Logic

The CI/CD pipeline has been completely restructured to follow your requirements:

```
STEP 1: Integration Tests + Spec Validation (parallel) ⚡
        ↓ (both must pass)
STEP 2: Deploy API Gateway 🚀
        ↓ (if succeeded)
STEP 3: Build SDK 📦
        ↓ (if succeeded)
STEP 4: Bump Version 🔢
        ↓ (if succeeded)
STEP 5: Publish SDK + Collection + Spec (parallel) ⚡
```

---

## 🔄 Workflow Stages

### **STEP 1: Validate Everything First** ⚡ (Parallel)

#### **1a. Integration Tests**
- Runs pytest on core-api
- Validates business logic
- Ensures API functionality

#### **1b. Generate & Validate Spec**
- Generates OpenAPI spec from FastAPI code
- Validates spec structure (syntax)
- **Validates against Postman governance rules** ⭐
- **Validates against Postman security rules (OWASP)** ⭐
- Uploads spec as artifact for later use
- **Blocks deployment if validation fails** (fail-severity: ERROR)

**Both must pass to proceed!**

---

### **STEP 2: Deploy API Gateway** 🚀

- Builds Docker image for API Gateway
- Deploys to production (TODO: add actual deployment)
- Only runs if tests AND spec validation pass

---

### **STEP 3: Build SDK** 📦

- Downloads pre-validated OpenAPI spec artifact
- Builds TypeScript SDK with LibLab
- Uploads SDK artifact
- Only runs if gateway deployed successfully

---

### **STEP 4: Bump Version** 🔢

- Reads current version
- Bumps patch version
- Commits version change
- Creates git tag
- Pushes to main
- Only runs if SDK built successfully

---

### **STEP 5: Publish Everything** ⚡ (Parallel)

All three jobs run simultaneously:

#### **5a. Publish SDK to npm**
- Downloads SDK artifact
- Publishes to npm registry
- Package: `@spearmint-finance/sdk`

#### **5b. Create Postman Collection**
- Creates collection in Postman workspace
- Uses new version number
- Configured for `https://api.spearmint.ai`

#### **5c. Publish Spec to Postman Spec Hub**
- Downloads OpenAPI spec artifact
- Publishes to Postman Spec Hub
- Uses new version number

---

## 🆚 Before vs After

### **Before (Old Logic):**
```
Tests → Build Gateway ↘
                       → Bump Version → Publish SDK
Tests → Build SDK    ↗                → Create Collection
                                       → Publish Spec
        (Spec validation was after SDK build and didn't block)
```

### **After (New Logic):**
```
Tests ↘
       → Deploy Gateway → Build SDK → Bump Version → Publish SDK ↘
Spec  ↗                                            → Collection  → Done
                                                   → Spec       ↗
```

---

## ✨ Key Improvements

### **1. Validate Before Deploy** ✅
- Spec validation now happens FIRST
- Catches governance/security issues before deploying
- Prevents bad specs from reaching production

### **2. Fail Fast** ⚡
- Validation failures stop the workflow immediately
- No wasted time building/deploying invalid specs
- Faster feedback loop

### **3. Cleaner Dependencies** 🎯
- Linear flow: Validate → Deploy → Build → Publish
- Clear separation of concerns
- Each step depends on previous success

### **4. Parallel Execution** 🚀
- Tests + Spec validation run in parallel (Step 1)
- SDK + Collection + Spec publishing run in parallel (Step 5)
- Faster overall workflow execution

### **5. Single Source of Truth** 📄
- Spec is generated and validated once
- Same validated spec used for SDK build and publishing
- No duplicate spec generation

---

## 🔒 Validation Now Blocks Deployment

**Important Change:**
- **Before:** Spec validation was informational (didn't block)
- **After:** Spec validation BLOCKS deployment on ERROR severity

**Fail Severity:** `ERROR`
- `HINT` - Informational suggestions (won't fail)
- `INFO` - Minor issues (won't fail)
- `WARNING` - Potential problems (won't fail)
- `ERROR` - Critical violations (**WILL FAIL** ❌)

---

## 📊 Workflow Jobs

| Job Name | Depends On | Runs When | Purpose |
|----------|-----------|-----------|---------|
| `integration-tests` | - | Always | Run pytest tests |
| `generate-and-validate-spec` | - | Always | Generate & validate OpenAPI spec |
| `deploy-gateway` | Tests + Spec validation | Both pass | Deploy API to production |
| `build-sdk` | Gateway deployment | Gateway deployed | Build TypeScript SDK |
| `bump-version` | SDK build | SDK built | Increment version |
| `publish-sdk` | Version bump | Version changed | Publish to npm |
| `create-postman-collection` | Version bump | Version changed | Create Postman collection |
| `publish-spec` | Version bump | Version changed | Publish to Spec Hub |

---

## 🎯 Benefits

✅ **Catch issues early** - Validation before deployment  
✅ **Fail fast** - Stop immediately on validation errors  
✅ **Faster feedback** - Parallel execution where possible  
✅ **Cleaner flow** - Linear dependency chain  
✅ **Single spec** - Generated once, used everywhere  
✅ **Governance enforcement** - Postman rules block bad specs  
✅ **Security compliance** - OWASP checks prevent vulnerabilities  

---

## 🚀 What Happens on Push

1. **Push to main** triggers workflow
2. **Tests + Spec validation** run in parallel
3. If **both pass** → Deploy gateway
4. If **gateway deployed** → Build SDK
5. If **SDK built** → Bump version
6. If **version changed** → Publish SDK + Collection + Spec (parallel)
7. **Done!** ✅

If **any step fails** → Workflow stops ❌

---

## 📋 Next Steps

1. **Watch the workflow run** - See the new structure in action
2. **Fix any spec violations** - Address governance/security issues
3. **Monitor validation results** - Check GitHub Actions summaries
4. **Adjust fail severity** - Change from ERROR to WARNING if needed

---

**The workflow is running now!** 🚀

Watch it at: https://github.com/spearmint-finance/spearmint/actions

You'll see the new parallel execution and linear dependency flow!

