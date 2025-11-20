# Spearmint Core API Endpoints

This document serves as an internal reference for the Core API endpoints, grouping them by domain and explaining their business purpose.

## 1. Transactions Domain
**Router:** `routes/transactions.py`

| Method | Endpoint | Purpose |
|:---|:---|:---|
| `GET` | `/transactions` | List transactions with filtering (date, category, type) and pagination. |
| `POST` | `/transactions` | Create a single transaction manually. |
| `GET` | `/transactions/{id}` | Get details for a specific transaction. |
| `PUT` | `/transactions/{id}` | Update transaction details (amount, description, category). |
| `DELETE` | `/transactions/{id}` | Soft delete a transaction. |
| `POST` | `/transactions/{id}/split` | Split a transaction across multiple people or categories. |

## 2. Accounts Domain
**Router:** `routes/accounts.py`

| Method | Endpoint | Purpose |
|:---|:---|:---|
| `GET` | `/accounts` | List all active financial accounts. |
| `POST` | `/accounts` | Create a new account (Checking, Savings, Credit Card). |
| `GET` | `/accounts/{id}/balances` | Get historical balance snapshots for a chart. |
| `POST` | `/accounts/{id}/reconcile` | Start a reconciliation session (compare Statement vs Calculated). |

## 3. Classification Engine
**Router:** `routes/classifications.py`

| Method | Endpoint | Purpose |
|:---|:---|:---|
| `GET` | `/classifications` | List available classification types (e.g., "Standard", "Transfer", "Refund"). |
| `GET` | `/classification-rules` | List the automation rules used to tag transactions. |
| `POST` | `/classification-rules` | Create a new pattern-matching rule. |
| `POST` | `/classification-rules/test` | Dry-run a rule against the DB to see what it would catch. |
| `POST` | `/classification-rules/apply` | **Batch Job:** Apply all active rules to unclassified transactions. |

## 4. Reporting & Analytics
**Router:** `routes/reports.py`

| Method | Endpoint | Purpose |
|:---|:---|:---|
| `GET` | `/reports/summary` | High-level dashboard data (Income vs Expense, Top Categories). |
| `GET` | `/reports/income` | Detailed income breakdown by category. |
| `GET` | `/reports/expenses` | Detailed expense breakdown by category. |
| `GET` | `/reports/cashflow` | Monthly cash flow trend analysis. |
| `GET` | `/reports/balances` | **Net Worth Report:** Current balance of all accounts, grouped by Asset/Liability. |
| `GET` | `/reports/reconciliation` | Audit log of all transactions including transfers (Complete Mode). |

## 5. System Maintenance
**Router:** `routes/maintenance.py`

Endpoints for fixing data consistency issues (migrated from legacy scripts).

| Method | Endpoint | Purpose |
|:---|:---|:---|
| `POST` | `/maintenance/fix/classifications` | Repairs system classifications (e.g., ensures "Insurance Reimbursement" is handled correctly). |
| `POST` | `/maintenance/fix/transfers` | **Batch Job:** Detects and links orphaned transfers between accounts. |
| `POST` | `/maintenance/fix/reimbursements` | **Batch Job:** Links expense reimbursements to their income counterparts. |

## 6. Import Workflow
**Router:** `routes/import_routes.py`

| Method | Endpoint | Purpose |
|:---|:---|:---|
| `POST` | `/import/upload` | Upload a CSV/Excel file from a bank. |
| `POST` | `/import/preview` | Preview how the parser interprets the file columns. |
| `POST` | `/import/confirm` | Commit the imported data to the `transactions` table. |

## 7. Projections (Scenarios)
**Router:** `routes/projections.py`, `routes/scenarios.py`

| Method | Endpoint | Purpose |
|:---|:---|:---|
| `GET` | `/projections/forecast` | Predict future account balances based on historical average spending. |
| `POST` | `/scenarios/preview` | Run a "What If" analysis (e.g., "What if I lose my job in June?") without saving data. |
