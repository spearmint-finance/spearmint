# Demo Script: API-First Development with Automated Validation & Deployment

**Product:** Spearmint Finance | **Duration:** ~15 minutes | **Updated:** 2026-03-13

---

## Demo Overview

Walk through the full lifecycle of adding a new API endpoint — from writing code to production deployment — showing how every stage is validated, tested, and automated.

**Story:** We're implementing the Scenario Creation API from our new PRD. A user wants to create a custom "Having a Baby" scenario with multiple financial adjusters. We'll build the endpoint, validate it locally, push to CI, and watch the full pipeline run.

**Key themes:**
- API-first design with OpenAPI spec generation
- Shift-left validation (catch issues before they hit CI)
- Postman governance & security rules enforcement
- Automated SDK generation and Postman collection updates

---

## Act 1: The Starting Point (~2 min)

### What to show

1. **Open the Scenarios page** in the running app (http://localhost:5173/scenarios)
   - Show existing scenario functionality — users can preview and save single-adjuster scenarios
   - Point out the gap: no way to create multi-adjuster scenarios or use templates

2. **Open the PRD** (`demo/scenario-creation-prd.md`)
   - Briefly highlight the key requirement: users need a scenario builder with templates and multi-adjuster support
   - Call out FR-1 (Scenario Builder) and FR-2 (Adjuster Types) as what we're building today

3. **Show the current OpenAPI spec** (`sdk/openapi.json`)
   - Point out existing scenario endpoints
   - Note that there's no endpoint for creating custom multi-adjuster scenarios

### Talking points

> "Today we're going to add a new API endpoint and walk through our entire validation and deployment pipeline. Every step — from local development to production — has automated quality gates powered by Postman."

---

## Act 2: Write the New API Endpoint (~3 min)

### What to show

1. **Add the new endpoint** in the backend
   - Open `core-api/src/financial_analysis/api/routes/scenarios.py`
   - Add a new `POST /api/scenarios/create` endpoint with the schema from the PRD
   - Include Pydantic schemas for the request body (scenario name, description, adjusters array)
   - Show the adjuster types: Income Change, Expense Addition, Expense Change, One-Time Cost

2. **Show the schema design**
   - Walk through the request/response models
   - Point out validation rules: name required, 1-20 adjusters, valid adjuster types
   - Highlight that this is standard FastAPI — the OpenAPI spec is auto-generated from the code

### Talking points

> "With FastAPI, our OpenAPI spec is generated directly from the code. The Pydantic models we write become the schema definitions. This means the spec is always in sync with the implementation — no manual spec editing."

---

## Act 3: Local Validation with Pre-Commit Hooks (~3 min)

### What to show

1. **Stage the changes and attempt a commit**
   ```bash
   git add core-api/src/financial_analysis/api/routes/scenarios.py
   git commit -m "feat(scenarios): add custom scenario creation endpoint"
   ```

2. **Watch the pre-commit hook run** — it triggers the full API Validation Suite:
   - **Step 1: OpenAPI Generation** — Regenerates `sdk/openapi.json` from the FastAPI app
   - **Step 2: Structural Validation** — Validates the spec against the OpenAPI 3.x schema
   - **Step 3: Postman Governance & Security Rules** — Runs Postman CLI validation against the workspace governance rules (API design standards + OWASP API Security Top 10)

3. **If validation fails** (good for demo — intentionally leave off a response description):
   - Show the error output: which rule failed, the path, the severity
   - Fix the issue in the code
   - Re-commit and show it passing

4. **If validation passes:**
   - Show the green output: all three validation stages passed
   - The spec file (`sdk/openapi.json`) is regenerated and staged automatically

### Talking points

> "This is shift-left validation. Before code ever leaves the developer's machine, we validate the OpenAPI spec against Postman's governance and security rules. If you introduce an endpoint without proper error responses, or missing authentication — it gets caught right here, not in code review."

### Key files to reference

- `.pre-commit-config.yaml` — Hook configuration
- `core-api/scripts/api_validation/run_all_validations.py` — Orchestrator that runs all three checks
- `core-api/scripts/api_validation/postman_validation.py` — Postman CLI integration

---

## Act 4: Push to CI — The Automated Pipeline (~4 min)

### What to show

1. **Push the commit to main**
   ```bash
   git push origin main
   ```

2. **Open GitHub Actions** and show the pipeline kick off
   - URL: `https://github.com/spearmint-finance/spearmint/actions`

3. **Walk through each job as it runs:**

   | Job | What it does | Duration |
   |-----|-------------|----------|
   | **generate-and-validate-spec** | Regenerates OpenAPI spec, runs structural validation, runs Postman governance & security validation | ~1 min |
   | **integration-tests** | Runs `pytest` against the full API (runs in parallel with spec validation) | ~1 min |
   | **deploy-gateway** | Builds and deploys the API gateway Docker image | ~10s |
   | **generate-mcp-tools** | Regenerates MCP server tools from the updated OpenAPI spec | ~1.5 min |
   | **build-sdk** | LibLab generates TypeScript + Python SDKs from the OpenAPI spec | ~1 min |
   | **bump-version** | Auto-increments version, creates git tag, pushes | ~10s |
   | **publish-sdk** | Publishes the TypeScript SDK to npm (`@spearmint-finance/sdk`) | ~45s |
   | **publish-spec-and-collection** | Updates the Postman spec and collection in-place, forks previous version as archive | ~20s |

4. **Click into the spec validation job** and show the GitHub Actions summary:
   - The validation results table showing governance and security checks
   - All checks green

5. **Click into the build-sdk job** and show LibLab generating the SDK:
   - The new scenario creation endpoint is now available in the TypeScript and Python SDKs

### Talking points

> "The same Postman validation that ran locally now runs again in CI — this is our safety net. Even if someone bypasses the pre-commit hook, CI will catch it. And notice the integration tests run in parallel with spec validation — we're not slowing down the pipeline."

> "After validation passes, the pipeline automatically generates a new SDK with the scenario creation method, bumps the version, and publishes to npm. No manual steps."

---

## Act 5: Postman Collection & Spec Update (~2 min)

### What to show

1. **Open Postman** and navigate to the Spearmint workspace

2. **Show the updated spec** in Postman's API hub
   - The new `POST /api/scenarios/create` endpoint is now in the spec
   - Schema definitions for the request body and response are populated
   - Point out the version number matches the git tag

3. **Show the updated collection**
   - The scenarios folder now includes the new endpoint
   - Request body is pre-populated from the spec
   - Examples show success and validation error responses

4. **Show the version archive**
   - Previous version was forked to the archive workspace before the update
   - Full version history available through Postman forks

5. **Run the scenario creation request** from Postman
   - Send a test request creating a "Having a Baby" scenario with multiple adjusters
   - Show the successful response

### Talking points

> "The production Postman collection is always in sync with the deployed API. When we pushed code, the pipeline updated the spec, the collection, and archived the previous version — all automatically. The team can start testing the new endpoint in Postman immediately."

---

## Act 6: The Published SDK (~1 min)

### What to show

1. **Show the npm package** — `@spearmint-finance/sdk` with the new version

2. **Show a quick code snippet** using the new SDK method:
   ```typescript
   import { SpearmintApi } from '@spearmint-finance/sdk';

   const client = new SpearmintApi({ token: 'Bearer ...' });

   const scenario = await client.scenarios.create({
     name: "Having a Baby",
     description: "Model financial impact of expanding our family",
     adjusters: [
       { type: "income_change", category: "Salary", percent_change: -100, start_date: "2026-07-01", end_date: "2026-09-30" },
       { type: "expense_addition", name: "Childcare", category: "Childcare", monthly_amount: 1800, start_date: "2026-10-01" },
       { type: "one_time_cost", name: "Hospital", amount: 5000, date: "2026-08-15", category: "Medical" }
     ]
   });
   ```

3. **Point out** that this SDK method was auto-generated — nobody wrote this client code manually

### Talking points

> "From writing a Python endpoint to having a published TypeScript SDK with full type safety — completely automated. The SDK, the Postman collection, and the OpenAPI spec are always in sync because they all flow from the same source of truth: the code."

---

## Recap & Key Takeaways (~1 min)

### The pipeline at a glance

```
Code → Pre-commit (Postman validation) → Push → CI Pipeline
                                                    ├── Spec generation + validation (Postman governance & security)
                                                    ├── Integration tests
                                                    ├── SDK generation (LibLab)
                                                    ├── Version bump + git tag
                                                    ├── Publish SDK to npm
                                                    └── Update Postman spec + collection
```

### Key points to land

1. **API-first, code-generated** — OpenAPI spec is generated from FastAPI code, never hand-edited
2. **Shift-left validation** — Postman governance & security rules run locally via pre-commit hooks before code is pushed
3. **CI enforcement** — Same validation runs again in the pipeline as a safety net
4. **Automated publishing** — SDK, Postman collection, and spec are all updated automatically on every merge to main
5. **Version history** — Every release is archived in Postman via collection forks and git tags

---

## Pre-Demo Checklist

- [ ] Backend running on `localhost:8000`
- [ ] Frontend running on `localhost:5173`
- [ ] `pre-commit` installed and hooks active (`pre-commit install`)
- [ ] Postman CLI authenticated (`postman login`)
- [ ] GitHub Actions secrets configured (`LIBLAB_TOKEN`, `POSTMAN_API_KEY`, `NPM_TOKEN`)
- [ ] Postman workspace open in browser
- [ ] Terminal visible alongside the editor
- [ ] Demo branch created (avoid pushing directly to main during live demo)
- [ ] Patch file verified: `git apply --check demo/code/scenario-templates.patch`
- [ ] Code is in clean/reverted state (no template endpoint present)

---

## Appendix A: Applying & Reverting the Demo Code

The new scenario templates endpoint is stored as a git patch file so it can be applied instantly during the demo — simulating a real coding experience without the risk of typos or missed files.

**Patch file:** `demo/code/scenario-templates.patch`

### What the patch adds

| File | Changes |
|------|---------|
| `core-api/src/financial_analysis/api/schemas/scenario.py` | Adds `TemplateAdjuster`, `ScenarioTemplate`, and `ScenarioTemplateListResponse` Pydantic models |
| `core-api/src/financial_analysis/api/routes/scenarios.py` | Adds `GET /api/scenarios/templates` endpoint with pagination, plus 6 seed templates (Having a Baby, Buying a Home, Job Change, Tax Increase, Early Retirement, Starting a Business) |

### Before the demo — verify clean state

```bash
# Confirm the patch applies cleanly (dry run, no changes made)
git apply --check demo/code/scenario-templates.patch
```

### During the demo (Act 2) — apply the code

```bash
# Apply the patch — changes appear instantly in the IDE
git apply demo/code/scenario-templates.patch
```

Then walk through the changed files in the IDE to explain what was added.

### After the demo — reset to clean state

```bash
# Revert the patch
git apply --reverse demo/code/scenario-templates.patch

# Commit and push the revert so CI rolls back Postman + SDK too
git commit -am "chore: reset demo"
git push
```

### Quick test after applying

```bash
# Verify the endpoint works
curl -s http://localhost:8000/api/scenarios/templates | python -m json.tool
```

Expected: paginated JSON with 6 templates, each containing an `adjusters` array.
