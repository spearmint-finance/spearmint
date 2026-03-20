# Competitive Analysis — March 2026

**Date:** 2026-03-20
**Author:** Product Team
**Purpose:** Benchmark Spearmint against market alternatives to identify competitive gaps and advantages.

---

## Market Segments

### 1. Open Source Self-Hosted (Direct Competitors)

| App | Strengths | Weaknesses | Spearmint Advantage |
|-----|-----------|------------|---------------------|
| **Firefly III** | Mature, large community (14k+ stars), multi-currency, rule automation, Plaid-like importers | PHP/Laravel stack, dated UI, no forecasting, no CapEx separation | Modern React UI, CapEx/OpEx separation, forecasting, AI assistant |
| **Actual Budget** | Envelope budgeting, clean UI, local-first, growing community (15k+ stars) | Budget-focused only, no investment tracking, no reports beyond budget | Full accounting depth: reports, analysis, reconciliation, investment holdings |
| **GnuCash** | Full double-entry accounting, decades mature | Desktop-only, steep learning curve, no web UI | Web-based, Docker deployment, consumer-friendly UX |
| **Beancount/Fava** | Plain-text accounting, powerful queries | CLI/text-file workflow, developer-only audience | Accessible to non-developers, visual dashboard |

### 2. Paid Consumer Apps (Indirect Competitors)

| App | Monthly Cost | Strengths | Spearmint Advantage |
|-----|-------------|-----------|---------------------|
| **Monarch Money** | $15/mo | Plaid integration, clean UI, investment tracking | Free, self-hosted, data sovereignty |
| **YNAB** | $15/mo | Best-in-class budgeting, envelope method, community | Free, CapEx separation, professional reporting |
| **Copilot** | $15/mo | AI categorization, Apple-quality UI | Free, open source, cross-platform |
| **Lunch Money** | $10/mo | Developer-friendly, API, multi-currency | Free, self-hosted, more analytical depth |

### 3. Deprecated

| App | Status | Opportunity |
|-----|--------|-------------|
| **Mint** | Shut down (2024) | 3.6M displaced users seeking alternatives |

---

## Competitive Gap Analysis

### Critical Gaps (Must close for G1)

| Gap | Competitors with this | Impact | Priority |
|-----|----------------------|--------|----------|
| **No authentication** | All competitors have auth | Cannot be used in any shared/networked environment. Fatal for real-world adoption. | P0 |
| **No budget management UI** | YNAB, Actual Budget, Monarch, Firefly III | Budgeting is the #1 use case for personal finance apps. Without it, we lose the largest user segment. | P1 |

### Important Gaps (Should close for G2)

| Gap | Competitors with this | Impact | Priority |
|-----|----------------------|--------|----------|
| **No bank linking** | Monarch, YNAB, Copilot, Lunch Money, Firefly III (via importers) | Manual CSV import is acceptable for V1 audience but limits mass adoption. | P2 |
| **Scenario builder incomplete** | Monarch (basic), Copilot (projections) | Core differentiator from vision doc — currently stubbed. | P2 |
| **No confidence intervals in forecasting** | None (this is our unique differentiator) | Opportunity to lead rather than follow. | P2 |

### Competitive Advantages (Protect and Promote)

| Advantage | Description |
|-----------|-------------|
| **CapEx/OpEx separation** | No consumer competitor offers this. Our "Renovation Moment" user story is unique. |
| **Entity-scoped accounting** | Multi-entity support for business/personal/rental separation. Only GnuCash approaches this. |
| **7 report types** | Balance, summary, income detail, expense detail, reconciliation, capex, receivables — more than most competitors. |
| **AI assistant** | Built-in chat with action execution. Copilot has AI but not open-source. |
| **Investment holdings** | Portfolio tracking alongside checking/savings. Monarch and Copilot have this; Firefly III and Actual Budget do not. |
| **Free and self-hosted** | Zero recurring cost, full data sovereignty. Appeals to privacy-conscious and cost-sensitive users. |

---

## Recommendations

1. **Close auth gap immediately** — This is a P0 blocker. No other improvement matters if the app can't be securely deployed.
2. **Build budget management UI** — This is the single largest feature gap versus the competitive field. It converts Spearmint from an "analyst tool" to a "daily driver."
3. **Promote unique advantages in README** — CapEx separation, entity scoping, and AI assistant are genuine differentiators that should be front and center.
4. **Target Firefly III and Actual Budget users** — These are the closest competitors. Our modern stack, analytical depth, and AI features are compelling compared to their offerings.
