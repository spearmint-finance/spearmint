# Spearmint Product Capabilities

## 1. Overview
Spearmint is a personal finance platform designed to replace Mint.com, offering advanced capabilities for transaction tracking, automated classification, and financial forecasting.

## 2. Core Entities

### 2.1. Accounts
Tracks financial containers.
*   **Types:** Checking, Savings, Credit Card, Loan, 401k, Brokerage.
*   **Hybrid Support:** Unique capability to handle "Brokerage" accounts that contain both **Cash** (spending power) and **Investments** (Holdings).
*   **Reconciliation:** Built-in system to compare "Statement Balance" vs "Calculated Balance" to ensure data integrity.

### 2.2. Transactions
The atomic unit of financial activity.
*   **Splits:** A single transaction can be split across multiple people (`Person` entity) for shared household expense tracking.
*   **Transfers:** Explicit support for identifying transfers between internal accounts to avoid double-counting income/expense.
*   **Tags:** Flexible tagging system for ad-hoc organization.

## 3. Automation Engine (The "Brain")

Spearmint uses a dual-layer rule system to automate bookkeeping.

### 3.1. Categorization Rules
*   **Goal:** What *kind* of spending is this? (e.g., "Groceries", "Rent").
*   **Logic:** Matches patterns in Description, Source, Amount, or Payment Method.
*   **Hierarchy:** Categories can be nested (e.g., `Food` > `Groceries`).

### 3.2. Classification Rules
*   **Goal:** How should this affect my math?
*   **Logic:** Assigns high-level properties:
    *   `exclude_from_income_calc`: Is this a refund?
    *   `exclude_from_expense_calc`: Is this a reimbursement?
    *   `exclude_from_cashflow_calc`: Is this an internal transfer?
*   **Priority:** Rules have numeric priorities to resolve conflicts.

## 4. Financial Intelligence

### 4.1. Forecasting (Scenarios)
Users can define "Scenarios" (e.g., "Retire Early", "Job Loss") to project future net worth.
*   **Adjusters:** Events that modify the projection (e.g., "Income drops by 50% starting June 1st").
*   **Horizon:** Projects 12+ months into the future.

### 4.2. Reporting
*   **Net Worth:** Assets (Cash + Investments) - Liabilities (Credit Cards + Loans).
*   **Cash Flow:** Monthly Income vs Expenses (excluding transfers/reimbursements).

## 5. Data Pipeline

1.  **Import:** CSV / Bank Export ingestion (`ImportHistory`).
2.  **Clean:** Deduplication based on dates and amounts.
3.  **Classify:** Rule Engine runs to assign Categories and Classifications.
4.  **Verify:** User reviews "Uncategorized" or "Low Confidence" items.
5.  **Report:** Data flows into Dashboards and Scenarios.
