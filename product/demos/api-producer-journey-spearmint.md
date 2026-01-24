# API Producer Journey

**Enterprise Demo & Positioning Guide**

*Spearmint Personal Finance Engine Scenario*

---

> **Executive Summary**
>
> This document equips FDEs to deliver a compelling demo showing how Postman transforms the API producer journey. The demo follows the backend team at Spearmint—a self-hosted personal finance engine—as they build a real feature: Scenario-Based Financial Forecasting. It demonstrates how Postman eliminates the friction between design, development, and deployment while ensuring governance compliance.
>
> **Key Message:** Postman enables producers to ship governed, documented APIs in hours instead of weeks by embedding validation, testing, and compliance directly into the creation workflow.

---

## How to Use This Document

This document serves two purposes: a ready-to-deliver demo script and a template for future FDE enablement materials. Each phase follows a consistent structure to make both delivery and creation straightforward.

### Target Audience

**Primary:** Engineering Directors, VP Engineering, and CTOs evaluating API platform investments. These buyers care about developer velocity, governance at scale, and reducing time-to-production.

**Secondary:** Platform Engineering leads and Enterprise Architects responsible for API standards and tooling decisions.

### Section Structure

Each lifecycle phase uses this format:

- **The Problem** — What pain does your buyer experience today?
- **Why It Persists** — Root causes that keep teams stuck in manual processes
- **The Postman Solution** — How our platform addresses this specifically
- **Demo Steps** — Exact actions to show in the demo

### Success Criteria

A successful delivery of this demo achieves the following:

1. The buyer articulates back the design validation value proposition in their own words
2. The buyer asks follow-up questions about governance rule customization
3. The buyer requests a POC or trial to test with their own specifications
4. The buyer identifies internal stakeholders who should see this demo

---

## The Scenario: Spearmint

> **Story Setup**
>
> Spearmint is a self-hosted personal finance engine that helps users import bank transactions, classify expenses, and forecast their financial future. Users love the projections feature but keep asking: "What if I lose my job?" or "What if my rent increases by 20%?" The team needs to build Scenario-Based Financial Forecasting—letting users define hypothetical adjustments (income changes, expense shocks) and see how their runway and net worth would change over time. This complex feature involves statistical calculations, multi-series response data, and real-time scenario comparisons. The frontend team is blocked until the API contract is defined.

This scenario resonates because it mirrors real development pressure: a feature users are actively requesting, complex domain logic (financial projections with adjusters), cross-team dependencies between backend and frontend, and the need for governance compliance when handling financial data. Anyone who's wondered "can I afford this decision?" understands the value.

### Key Characters

| Role | Responsibility |
|------|----------------|
| Backend Developer | Designs and implements the Scenarios API |
| Platform Engineer | Ensures API follows governance standards |
| Frontend Developer | Will consume the API in the React web app |
| QA Engineer | Validates the implementation works correctly |

---

## Phase 0: Requirements & API Design Handoff

### The Problem

The Product team has documented user requirements in Confluence: users need "what-if" financial scenario modeling. The PRD explains the problem, user stories, and success criteria. But now the backend developer needs to translate these product requirements into API design decisions. What endpoints are needed? What should the request/response structure look like? How do user workflows map to API calls?

This handoff between product and engineering often breaks down. The backend developer reads the PRD once, then closes the tab and starts coding. Questions arise during implementation: "Should scenarios be saved or just previewed?" "What exactly goes in the response?" But the PRD is in Confluence, the API design happens in an IDE or OpenAPI editor, and the two never connect. Context gets lost, and the backend developer makes assumptions that diverge from user needs.

### Why It Persists

Product requirements and API technical specifications live in separate tools with no clear bridge:

- **No linking between product and technical docs.** The PRD lives in Confluence. The OpenAPI spec lives in GitHub. When the developer has questions during API design, they can't easily reference the user stories that motivated each endpoint.
- **Lost context during handoff.** The backend developer reads the PRD, extracts "build scenario forecasting," then works in isolation. The "why" behind user workflows gets forgotten.
- **Specifications drift from intent.** API design decisions (ephemeral vs. saved scenarios, response structure) get made without revisiting user needs. The API becomes technically correct but misaligned with how users actually think.
- **No shared workspace.** Product, backend, and frontend collaborate in Slack DMs and meetings rather than a persistent space where requirements and API design coexist.

### The Postman Solution

Postman workspaces bridge the gap between product requirements and API design. While the authoritative PRD lives in your product management tool (Confluence, Notion, Jira), the Postman workspace becomes the collaboration layer where engineering translates those requirements into API specifications.

Backend developers create a collection description that summarizes the PRD—user stories, key workflows, and technical constraints—and links back to the full PRD. This context lives alongside the API design, visible to frontend, QA, and platform engineers. When questions arise, everyone references the same requirements summary without leaving Postman. The API specification becomes grounded in user needs rather than disconnected from them.

### Demo Steps

*[Screenshot: Confluence PRD tab alongside Postman workspace]*

1. **Show the Confluence PRD.** Open the "Scenario-Based Financial Forecasting" PRD in Confluence (or your product management tool). Highlight the key sections:
   - User problem: "Users can't model what-if scenarios"
   - User stories: Job loss simulation, rent increase modeling, side-by-side comparison
   - Key user workflow: Define adjustment → see projections → save or discard
   - Success criteria: Answer "what-if" questions in under 30 seconds

2. **Switch to Postman workspace.** Open the Spearmint API workspace. "This is where engineering will design the Scenarios API based on the PRD."

3. **Create a new collection for Scenarios API.** Create a collection called "Scenarios API - v1.0" and open the collection description editor.

4. **Summarize PRD in collection description.** Add a markdown summary that includes:
   - **Link to full PRD:** `📋 [Full PRD: Scenario Forecasting](https://confluence.company.com/prd/scenarios)` *(use a real or example link)*
   - **User Stories Summary:**
     - "As a user, I want to simulate job loss to see how long my savings will last"
     - "As a user, I want to compare baseline vs. scenario side-by-side"
   - **Key Workflow:** User defines adjustment (type, date, magnitude) → system recalculates → user sees comparison
   - **Technical Constraints:**
     - Must integrate with existing projections engine
     - Read-only operations (no transaction data modification)
     - Sub-2-second response time

5. **Highlight the bridging value.** "Now when the backend developer designs endpoints, the user context is right here. Frontend sees the same requirements. When QA writes tests, they reference the same user stories. Everyone works from a shared understanding—the PRD is linked, not lost."

6. **Transition to API design (Phase 1).** "With requirements captured, the backend developer can now design the API endpoints. Should there be a preview endpoint? Yes—the workflow says 'experiment without saving.' Should the response include side-by-side comparison? Yes—users want to see baseline vs. scenario. The API design decisions flow directly from user needs."

> **Talking Point:** "The PRD lives in Confluence where Product manages it. But engineering doesn't work in Confluence—they work in Postman. By summarizing key requirements and linking to the source, the workspace becomes the bridge. Backend references user stories while designing endpoints. Frontend sees why the API is structured this way. Nobody is building in a vacuum, guessing what the user needs."

---

## Phase 1: Prototyping & Design Validation

### The Problem

With clear user requirements defined in Phase 0, the backend developer now needs to design endpoints for Scenario-Based Forecasting: a preview endpoint that simulates "what-if" scenarios without saving data, endpoints for saved scenarios, and integration with the existing projections engine. The frontend team is blocked—they can't build the scenario comparison visualization until they know the response structure. Will the API return separate series for baseline vs. scenario? How are "adjusters" (like "job loss in June") represented?

In practice, developers frequently skip the design phase and jump straight to code. This creates long feedback loops where misunderstandings surface only after significant development effort. The frontend team might expect an array of time-series points, while the backend returns a nested object with KPI summaries. These mismatches waste cycles.

### Why It Persists

Engineers choose to skip design for understandable reasons:

- **Code feels real.** Developers see immediate results in their IDE. Writing a specification feels like administrative work rather than engineering.
- **Misinterpreted Agile.** Teams read "working software over comprehensive documentation" as permission to skip specifications entirely.
- **Inadequate tooling.** Data from the Postman State of the API Report shows many developers avoid API-first workflows because they find schema creation difficult or tedious. They need a way to make the design phase as tangible and interactive as writing code.

### The Postman Solution

Postman transforms design from a documentation exercise into an interactive prototyping experience. Developers create "design" collections using form-based editing tools to define example requests and responses. From these examples, they generate mock servers that simulate working API behavior. The frontend team can start building against the mock immediately—real HTTP requests, real response structures—while backend implements the actual logic.

After stakeholders validate the design, developers convert the approved collection to an OpenAPI specification with a single click. This specification becomes the official contract—checked into source control to drive downstream implementation.

### Demo Steps

*[Screenshot: Postman workspace with Spearmint API collection showing Scenarios folder]*

1. **Open the Spearmint API workspace.** Navigate to the workspace containing the existing Transactions, Projections, and Reports collections. "This shared workspace gives the whole team visibility into all our APIs."

2. **Fork the Projections collection.** Create a copy to work in isolation. "This preserves the production version while I experiment with the new scenario endpoints."

3. **Add the Scenario endpoints.** Create new requests for the scenario feature:

| Endpoint | Purpose |
|----------|---------|
| `POST /api/scenarios/preview` | Simulate a what-if scenario without saving |
| `GET /api/scenarios` | List all saved scenarios |
| `POST /api/scenarios` | Save a scenario configuration |
| `GET /api/scenarios/{id}` | Get specific saved scenario |
| `DELETE /api/scenarios/{id}` | Delete a saved scenario |
| `POST /api/scenarios/{id}/run` | Re-run a saved scenario with fresh data |

4. **Define the preview request/response schema.** Add examples showing: adjusters array (each with type, start_date, percentage_change), baseline_series (date/balance pairs), scenario_series (modified projections), kpis object (runway_months, min_balance, coverage_by_person), and deltas (income/expense/net_cf differences).

5. **Generate mock server.** With one click, create a mock server that responds based on the examples. Send a test request to POST /api/scenarios/preview with a "job loss" adjuster and show the mock returning the comparison data.

6. **Share mock URL with frontend.** "The frontend team can now build the dual-line chart comparing baseline vs. scenario. Real HTTP requests, real response structures—they're unblocked while I implement the statistical calculations."

7. **Export to OpenAPI.** Convert the validated collection to an OpenAPI spec. Commit this to source control as the authoritative contract.

> **Talking Point:** "The backend developer designed the Scenarios API and unblocked the frontend team in 30 minutes. The frontend is already building the comparison chart against the mock while backend implements the projection calculations. Without Postman, frontend would be waiting days—or building against assumptions that turn out to be wrong."

---

## Phase 2: Standards Enforcement

### The Problem

Spearmint has API governance rules that ensure consistency across the codebase: all endpoints use kebab-case paths, response schemas follow consistent patterns, sensitive data (account balances, transaction amounts) follow specific formats, and all CRUD endpoints follow RESTful conventions. The platform engineer is responsible for enforcing these standards.

Enforcing these standards creates friction. The platform engineer reviews pull requests manually, which slows development. Developers view these reviews as nitpicking rather than helpful guidance. Because feedback arrives late—during PR review—fixing violations requires context-switching back to code that felt "done."

### Why It Persists

Governance typically functions as a gate rather than a guardrail. The rules live in a README or contributing guide that developers forget to check. Without automated feedback, compliance becomes a memory test. This forces the platform engineer to act as "police" during code review, creating friction between velocity and standards.

### The Postman Solution

Postman shifts governance left by embedding rules directly into the creation process. The platform engineer defines rule sets once, and Postman applies them automatically as developers design and build. Real-time linting displays errors and warnings as the producer types—similar to ESLint in your IDE—guiding them toward compliance immediately.

For teams with existing linting tools, Postman imports *Spectral files* (industry-standard JSON/YAML rule definitions) directly into the governance engine. The same rules enforce compliance in the CI/CD pipeline through the Postman CLI, blocking non-conforming code from reaching production.

### Demo Steps

*[Screenshot: Governance rule editor showing kebab-case and financial data format rules]*

1. **Open Governance Settings.** Navigate to the API Governance section. Show the platform engineer's "Spearmint API Standards" ruleset.

2. **Review existing rules.** Walk through the key rules: kebab-case for all path segments, required `generated_at` timestamps on report responses, financial amounts must use Decimal type, consistent error response schema with proper 5xx handlers.

3. **Trigger a path violation.** Return to the Scenarios spec and intentionally use camelCase: `/api/scenarioPreview` instead of `/api/scenarios/preview`. Show the real-time error appearing immediately.

4. **Fix inline.** Correct the path and show the error disappearing. "The developer learned the naming convention while working, not during a PR review two days later."

5. **Show CI/CD enforcement.** Reference the GitHub Actions workflow where the Postman CLI runs the same rules. "A spec that violates governance fails the build—it never makes it to main."

> **Talking Point:** "The platform engineer defines the rules once. Postman enforces them everywhere—in the editor, in the IDE, in the pipeline. No more 'please fix the path naming' comments on PRs. Developers learn standards as they work, not during review."

---

## Phase 3: Build & Testing

### The Problem

The backend developer turns the design into working FastAPI endpoints. They implement the projection calculations, wire up the adjuster logic, and connect to the existing projections service. The QA engineer needs to validate that the implementation matches the spec.

Manual translation of the interface into code introduces errors. Simple mistakes—a typo in `baseline_series` vs `baselineSeries`, returning the KPIs object with wrong field names—break the contract. The frontend discovers these mismatches when their chart rendering fails, leading to finger-pointing and wasted debugging time.

### Why It Persists

Even with a spec in the repo, it remains a passive reference document:

- **Context switching breaks focus.** Developers toggle between the spec and their code editor, increasing cognitive load.
- **No real-time feedback.** Engineers cannot see when they violate the contract during implementation.
- **Incentive misalignment.** "Ship the feature" trumps "match the spec." Contract testing becomes optional work.

### The Postman Solution

Postman bridges the gap between specification and implementation:

- **Contract test automation.** Postman automatically generates tests that validate the implementation against the spec. These tests verify response schemas, status codes, and required fields without manual test authoring.
- **Environment portability.** The same test collection runs against mock, local dev, staging, and production. Developers test locally before pushing; QA runs identical tests against staging.
- **SDK generation.** The generated @spearmint-finance/sdk includes typed methods like `scenarios.previewScenario()` and `scenarios.listScenarios()`—frontend gets a client that matches the spec by construction.

### Demo Steps

*[Screenshot: Generated contract tests with schema validation for Scenarios]*

1. **Generate contract tests.** Create a test collection from the Scenarios spec. Walk through the auto-generated assertions: response schema validation, required fields (baseline_series, scenario_series, kpis, deltas, generated_at), and status code verification.

2. **Run against mock.** Execute the test collection against the mock server to establish baseline. All tests pass—the mock matches the spec by definition.

3. **Switch to Local Dev environment.** Change the environment variable from "Mock" to "Local Dev" where Spearmint is running via Docker. Rerun the tests.

4. **Show a contract violation.** Intentionally have the implementation missing the `runway_months` field in the KPIs object. Run tests and show the specific failure: "Expected kpis to have property 'runway_months'."

5. **Fix and rerun.** Add the missing field in the FastAPI response model. Rerun tests, show all passing. "The contract test caught this before frontend discovered it when rendering the dashboard."

6. **(Bonus) Show generated SDK.** Open the @spearmint-finance/sdk output. Show the typed `previewScenario()` method that frontend will use. "The SDK matches the spec—frontend gets type safety for free."

> **Talking Point:** "The QA engineer didn't write a single test assertion by hand. Postman generated contract tests from the spec. When the implementation drifted—missing a KPI field—the tests caught it immediately. Frontend never saw a broken API."

---

## Phase 4: Deployment & Notification

### The Problem

The backend developer merges the Scenarios feature. Now they need to: deploy the new API version, update the documentation, regenerate the SDK, and notify the frontend team that the real API is ready. Each of these is a manual step that gets forgotten under deadline pressure.

Documentation gets stale because updating it is a separate task. The frontend team doesn't know the feature shipped until someone mentions it in standup. The SDK has to be manually regenerated and published. These gaps create confusion and slow down the overall delivery.

### Why It Persists

CI/CD platforms excel at moving code to servers, but they don't manage the "product" aspects of an API. They don't know who consumes the API, so they can't target notifications. They can regenerate docs, but someone has to configure that. The release process focuses on deployment, not developer experience.

### The Postman Solution

Postman streamlines release through workspace synchronization. When a developer merges changes, the CI/CD pipeline automatically updates the workspace and collections to match the current API version. It simultaneously publishes the latest documentation and regenerates the SDK. Monitors run against the deployed environment to verify uptime. The platform notifies workspace followers automatically.

### Demo Steps

*[Screenshot: GitHub Actions workflow showing Postman CLI stages]*

1. **Show pipeline configuration.** Open the `deploy-and-version.yml` GitHub Actions workflow. Highlight the stages: governance check, contract tests, deploy, SDK generation, workspace sync.

2. **Trigger a deployment.** Merge the Scenarios feature branch to main. Watch the pipeline execute each stage.

3. **Verify workspace update.** Return to Postman and refresh the workspace. Show the new Scenarios collection, updated documentation with all the scenario endpoints, and the new environment pointing to the deployed API.

4. **Check monitor status.** Open the monitor dashboard showing health checks against the deployed Scenarios endpoints. "We know immediately if something breaks."

5. **Show notification.** Display the automatic notification sent to workspace followers. "The frontend team knew the Scenarios API was live before I could even message them."

> **Talking Point:** "The code merged at 2:15 PM. By 2:18 PM, the workspace was updated, documentation was live, the SDK was regenerated, and frontend was notified. No 'hey, did you see we shipped that?' Slack messages. No stale docs. The release process is the documentation process."

---

## Outcomes: The Wow Moment

The Spearmint team transformed a feature request into a fully governed, documented, production-ready API in a single continuous loop. Frame these outcomes in terms your buyer cares about:

| Outcome | Business Impact |
|---------|-----------------|
| **Requirements linked to API design** | Backend developer designed endpoints with user context visible alongside the spec. PRD in Confluence stayed authoritative, but key user stories were accessible in the workspace. No guessing about ephemeral vs. saved scenarios—the workflow summary made it clear. |
| **Design validated before code** | Frontend started building the scenario comparison chart immediately against the mock. No waiting, no assumptions, no rework when the "real" API arrived. |
| **Governance as guardrail** | Zero PR comments about naming conventions or missing fields. Developers learned standards while working. Platform engineer stopped being the "style police." |
| **Contract tests generated** | QA didn't write assertions by hand. Contract drift was caught before frontend integration. The missing runway_months KPI was fixed before anyone saw a broken dashboard. |
| **Zero-drift deployment** | Documentation, collections, SDK, and notifications updated automatically on merge. No stale docs. No "did we ship that?" confusion. |

> **The Bottom Line**
>
> Spearmint shipped a governed, documented, production-ready Scenario-Based Forecasting API in days instead of weeks. Users can finally ask "what if I lose my job?" and see their projected runway change in real time. The team is already using the same workflow for the next features: Receivables Tracking and Confidence Interval enhancements.

---

## Required Demo Assets

Ensure these assets are prepared and accessible before delivering the demo:

| Asset | Description |
|-------|-------------|
| PRD in Confluence/Notion | Product requirements document in your product management tool (Confluence, Notion, etc.) showing user stories, workflows, success criteria. Include link that can be referenced during demo. |
| Spearmint Workspace | Postman workspace with Transactions, Projections, and Reports collections. The Scenarios collection should have a description that summarizes the PRD and links to it. |
| Scenarios Collection | The collection with all scenario endpoints. Include intentional governance violation (camelCase path) for demo. |
| Mock Server | Pre-configured with scenario examples: "Job Loss", "Rent Increase", and "Early Retirement" adjusters. |
| Local Dev Environment | Spearmint running via Docker for live testing. Include version with missing runway_months KPI for contract violation demo. |
| GitHub Actions Workflow | The deploy-and-version.yml showing CI/CD integration with Postman CLI stages. |
| SDK Output | The generated @spearmint-finance/sdk package showing typed scenario methods. |
| Governance Rules | Spearmint API Standards ruleset: kebab-case paths, required timestamps, Decimal financial amounts, error schema. |

---

## Alternative Demo Scenarios

If you want variety or need to tailor the demo to a specific conversation, these alternative Spearmint features work equally well:

### Scenario B: Receivables & Reimbursement Tracking

Building the "Shadow Ledger" for money owed to the user:

- **Design:** Add GET /api/reports/receivables endpoint showing outstanding reimbursements
- **Governance:** Ensure amount fields use proper Decimal formatting
- **Testing:** Validate receivables sum against tagged "Reimbursable" transactions
- **Deploy:** Update SDK with new reports methods

### Scenario C: Capital Expenditure (CapEx) Reporting

Separating operating expenses from asset investments:

- **Design:** Add `is_capex` flag to transactions, create /api/reports/capex endpoint
- **Governance:** Ensure CapEx transactions include required asset metadata
- **Testing:** Validate CapEx exclusion from operating expense calculations
- **Deploy:** Update workspace and notify dependent services

---

## Appendix: Code-First Workflows

While this document focuses on the design-first approach, Postman fully supports teams who prefer code-first workflows. For customers who generate OpenAPI specs from code annotations (like FastAPI's automatic schema generation), the governance and testing capabilities apply identically—the spec simply enters the workflow at a different point.

*See the Code-First Appendix document for detailed positioning and demo guidance for these customers.*
