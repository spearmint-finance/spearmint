# Product Gap Analysis: Vision vs. Reality

**Date:** November 20, 2025
**Status:** Draft
**Reference:** `product_vision.md` vs `core-api` implementation.

## 1. Executive Summary
The current Spearmint Core API provides a solid foundation for "Horizon 1" (Sovereign Foundation), with robust transaction management, categorization, and basic reporting. However, key differentiators for "Horizon 2" (Intelligent Analyst)—specifically regarding Capital Expenditure (CapEx) tracking and Reimbursement workflows—require API enhancements to fully realize the "Personal CFO" vision.

## 2. Critical Gaps (Horizon 1 & 2)

### 2.1. Capital Expenditures (CapEx) Tracking
*   **Vision:** "The Renovation Moment." Users toggle "CapEx" on a transaction. It disappears from *Operating Expenses* but appears in *Asset Investment*. It is **not** just excluded; it is re-categorized as a balance sheet transfer.
*   **Current State:** The API supports `exclude_from_expense_calc`. This effectively hides the transaction from the P&L.
*   **The Gap:** There is no specific "CapEx" report or bucket. The money just "vanishes" from the expense report.
*   **Required API Change:**
    *   Update `Transaction` model: Add `is_capex` boolean (or distinct classification).
    *   Update `ReportService`: Create `generate_capex_report` to sum these specific transactions.
    *   Update `SummaryReport`: Include `total_capex` alongside Income and Expense.

### 2.2. Reimbursements & Receivables
*   **Vision:** "The Work Trip Split." Mark as "Reimbursable." It moves to a "Receivables" widget (Shadow Ledger).
*   **Current State:** `fix_reimbursements.py` (legacy) exists, but no live API. Tags exist.
*   **The Gap:** The frontend has no endpoint to fetch "Outstanding Receivables."
*   **Required API Change:**
    *   New Endpoint: `GET /reports/receivables`.
    *   Logic: Sum transactions tagged "Reimbursable" (Expense) vs "Reimbursement" (Income) to show net amount owed to user.

### 2.3. Forecasting Confidence
*   **Vision:** "Confidence Slider (40%)." Split graph into "Safe Path" vs "Optimistic Path."
*   **Current State:** `projections.py` generates linear/moving average forecasts. `scenarios.py` allows discrete adjustments ("Job Loss").
*   **The Gap:** The API returns a single deterministic forecast series. It does not seem to support a "Confidence Interval" or multiple probability-weighted scenarios in one response.
*   **Required API Change:**
    *   Update `/projections/forecast`: Accept `confidence_level` param or return `upper_bound` / `lower_bound` series.

### 2.4. Import Mapping ("Universal Adapter")
*   **Vision:** "Map raw CSV headers to standard fields. System remembers this."
*   **Current State:** `/import/upload` assumes a fairly standard schema or relies on internal heuristics.
*   **The Gap:** No "Mapping Configuration" entity in the database to store "Chase Credit Card maps 'Posting Date' to 'Date'".
*   **Required API Change:**
    *   New Model: `ImportProfile` (stores header mappings).
    *   Update `/import`: Accept `profile_id` to apply saved mappings.

## 3. Recommendation Roadmap

### Phase 2.1 (Immediate Fixes)
1.  **CapEx:** Add `total_capex` to `/reports/summary`.
2.  **Receivables:** Create `/reports/receivables` endpoint.

### Phase 2.2 (Enhancements)
3.  **Import Profiles:** Schema migration to support saved column mappings.
4.  **Confidence Intervals:** Enhance `AnalysisService` to return probability ranges.

## 4. Conclusion
The Core API is ~85% feature-complete for V1. Addressing the CapEx and Receivables gaps is high priority to deliver on the specific user stories defined in the Vision.
