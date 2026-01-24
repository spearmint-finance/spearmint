# Scenario-Based Financial Forecasting API

**Version:** 1.0
**Status:** Design Specification
**Related PRD:** [scenario-forecasting-prd.md](./scenario-forecasting-prd.md)
**Last Updated:** 2026-01-23

---

## Overview

This document defines the API endpoints required to implement Scenario-Based Financial Forecasting as specified in the PRD. These endpoints enable users to create, preview, save, and manage "what-if" financial scenarios.

All endpoints follow existing API conventions:
- Base path: `/api/scenarios`
- JSON request/response bodies
- Standard error response format
- Classification-aware calculations (excludes transfers and internal transactions)

---

## Endpoint Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/scenarios/preview` | Preview a scenario without saving (ephemeral) |
| `POST` | `/api/scenarios` | Create and save a new scenario |
| `GET` | `/api/scenarios` | List all saved scenarios |
| `GET` | `/api/scenarios/{scenario_id}` | Get a specific saved scenario |
| `PUT` | `/api/scenarios/{scenario_id}` | Update a saved scenario's configuration |
| `DELETE` | `/api/scenarios/{scenario_id}` | Delete a saved scenario |
| `POST` | `/api/scenarios/{scenario_id}/refresh` | Re-run a saved scenario with current data |
| `GET` | `/api/scenarios/{scenario_id}/comparison` | Get baseline vs scenario comparison data |

---

## Common Models

### AdjusterType Enum

```json
{
  "enum": ["income_change", "expense_change"]
}
```

**Values:**
- `income_change` - Modify income by percentage or amount for a category
- `expense_change` - Modify expenses by percentage or amount for a category

### ScenarioAdjuster

Defines a single adjustment to apply to the baseline projection.

```json
{
  "type": "income_change | expense_change",
  "category_id": 5,
  "adjustment_type": "percentage | fixed_amount",
  "adjustment_value": -100.0,
  "start_date": "2026-06-01",
  "end_date": null
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | Yes | Adjuster type: `income_change` or `expense_change` |
| `category_id` | integer | No | Category to adjust (null = all categories of type) |
| `adjustment_type` | string | Yes | How to apply: `percentage` (-100 to +1000) or `fixed_amount` |
| `adjustment_value` | number | Yes | Adjustment value (negative for decreases) |
| `start_date` | date | Yes | When adjustment begins (ISO 8601 format) |
| `end_date` | date | No | When adjustment ends (null = indefinite) |

### SeriesPoint

A single data point in a projection series.

```json
{
  "date": "2026-06-01",
  "balance": 15000.00,
  "income": 5000.00,
  "expenses": 4200.00,
  "net_cash_flow": 800.00
}
```

### ScenarioMetrics

Key performance indicators for a scenario.

```json
{
  "runway_months": 18.5,
  "min_balance": 2500.00,
  "min_balance_date": "2026-09-15",
  "total_income": 60000.00,
  "total_expenses": 50400.00,
  "total_net_cash_flow": 9600.00,
  "average_monthly_income": 5000.00,
  "average_monthly_expenses": 4200.00
}
```

### ComparisonDeltas

Differences between baseline and scenario projections.

```json
{
  "runway_months_delta": -5.2,
  "min_balance_delta": -8500.00,
  "total_income_delta": -30000.00,
  "total_expenses_delta": 0.00,
  "total_net_cash_flow_delta": -30000.00
}
```

### ErrorResponse

Standard error response format.

```json
{
  "detail": "Scenario not found",
  "error_code": "SCENARIO_NOT_FOUND",
  "timestamp": "2026-01-23T10:30:00Z"
}
```

---

## Endpoints

### 1. Preview Scenario (Ephemeral)

**`POST /api/scenarios/preview`**

Simulate a scenario without saving it. Use for rapid iteration and exploration.

**Performance Requirement:** < 2 seconds (p95)

#### Request Body

```json
{
  "name": "Job Loss Scenario",
  "description": "What if I lose my job in June?",
  "horizon_months": 12,
  "starting_balance": 25000.00,
  "adjusters": [
    {
      "type": "income_change",
      "category_id": 1,
      "adjustment_type": "percentage",
      "adjustment_value": -100.0,
      "start_date": "2026-06-01",
      "end_date": null
    }
  ]
}
```

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `name` | string | No | null | Display name for the preview |
| `description` | string | No | null | Description of the scenario |
| `horizon_months` | integer | No | 12 | Projection horizon (1-60 months) |
| `starting_balance` | number | No | 0.00 | Starting account balance |
| `adjusters` | array | Yes | [] | List of adjustments to apply |

#### Response (200 OK)

```json
{
  "baseline_series": [
    {
      "date": "2026-02-01",
      "balance": 26500.00,
      "income": 5500.00,
      "expenses": 4000.00,
      "net_cash_flow": 1500.00
    },
    {
      "date": "2026-03-01",
      "balance": 28000.00,
      "income": 5500.00,
      "expenses": 4000.00,
      "net_cash_flow": 1500.00
    }
  ],
  "scenario_series": [
    {
      "date": "2026-02-01",
      "balance": 26500.00,
      "income": 5500.00,
      "expenses": 4000.00,
      "net_cash_flow": 1500.00
    },
    {
      "date": "2026-03-01",
      "balance": 28000.00,
      "income": 5500.00,
      "expenses": 4000.00,
      "net_cash_flow": 1500.00
    },
    {
      "date": "2026-06-01",
      "balance": 28500.00,
      "income": 0.00,
      "expenses": 4000.00,
      "net_cash_flow": -4000.00
    }
  ],
  "baseline_metrics": {
    "runway_months": null,
    "min_balance": 25000.00,
    "min_balance_date": "2026-02-01",
    "total_income": 66000.00,
    "total_expenses": 48000.00,
    "total_net_cash_flow": 18000.00,
    "average_monthly_income": 5500.00,
    "average_monthly_expenses": 4000.00
  },
  "scenario_metrics": {
    "runway_months": 7.1,
    "min_balance": 0.00,
    "min_balance_date": "2026-12-15",
    "total_income": 27500.00,
    "total_expenses": 48000.00,
    "total_net_cash_flow": -20500.00,
    "average_monthly_income": 2291.67,
    "average_monthly_expenses": 4000.00
  },
  "deltas": {
    "runway_months_delta": -999,
    "min_balance_delta": -25000.00,
    "total_income_delta": -38500.00,
    "total_expenses_delta": 0.00,
    "total_net_cash_flow_delta": -38500.00
  },
  "generated_at": "2026-01-23T10:30:00Z"
}
```

#### Error Responses

| Status | Error Code | Description |
|--------|------------|-------------|
| 400 | `INVALID_ADJUSTER` | Invalid adjuster configuration |
| 400 | `INVALID_DATE_RANGE` | start_date must be before end_date |
| 400 | `INSUFFICIENT_HISTORY` | Less than 3 months of transaction history |
| 422 | `VALIDATION_ERROR` | Request body validation failed |

---

### 2. Create Scenario

**`POST /api/scenarios`**

Create and save a new scenario for future reference.

#### Request Body

```json
{
  "name": "Job Loss - June 2026",
  "description": "Scenario modeling complete job loss starting June 2026",
  "horizon_months": 12,
  "starting_balance": 25000.00,
  "adjusters": [
    {
      "type": "income_change",
      "category_id": 1,
      "adjustment_type": "percentage",
      "adjustment_value": -100.0,
      "start_date": "2026-06-01",
      "end_date": null
    }
  ]
}
```

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `name` | string | Yes | - | Unique name for the scenario |
| `description` | string | No | null | Description of the scenario |
| `horizon_months` | integer | No | 12 | Projection horizon (1-60 months) |
| `starting_balance` | number | No | 0.00 | Starting account balance |
| `adjusters` | array | Yes | - | List of adjustments to apply |

#### Response (201 Created)

```json
{
  "id": 1,
  "name": "Job Loss - June 2026",
  "description": "Scenario modeling complete job loss starting June 2026",
  "horizon_months": 12,
  "starting_balance": 25000.00,
  "adjusters": [
    {
      "type": "income_change",
      "category_id": 1,
      "category_name": "Salary",
      "adjustment_type": "percentage",
      "adjustment_value": -100.0,
      "start_date": "2026-06-01",
      "end_date": null
    }
  ],
  "created_at": "2026-01-23T10:30:00Z",
  "updated_at": "2026-01-23T10:30:00Z",
  "last_run_at": "2026-01-23T10:30:00Z"
}
```

#### Error Responses

| Status | Error Code | Description |
|--------|------------|-------------|
| 400 | `INVALID_ADJUSTER` | Invalid adjuster configuration |
| 400 | `DUPLICATE_NAME` | Scenario with this name already exists |
| 422 | `VALIDATION_ERROR` | Request body validation failed |

---

### 3. List Scenarios

**`GET /api/scenarios`**

Retrieve all saved scenarios with metadata.

**Performance Requirement:** < 500ms (p95)

#### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `limit` | integer | No | 50 | Maximum results to return (1-100) |
| `offset` | integer | No | 0 | Number of results to skip |
| `sort_by` | string | No | `updated_at` | Sort field: `name`, `created_at`, `updated_at`, `last_run_at` |
| `sort_order` | string | No | `desc` | Sort direction: `asc` or `desc` |

#### Response (200 OK)

```json
{
  "scenarios": [
    {
      "id": 1,
      "name": "Job Loss - June 2026",
      "description": "Scenario modeling complete job loss starting June 2026",
      "horizon_months": 12,
      "adjuster_count": 1,
      "adjuster_summary": "Income: -100% Salary from Jun 2026",
      "created_at": "2026-01-23T10:30:00Z",
      "updated_at": "2026-01-23T10:30:00Z",
      "last_run_at": "2026-01-23T10:30:00Z",
      "is_stale": false
    },
    {
      "id": 2,
      "name": "Rent Increase 2026",
      "description": "Model 20% rent increase starting March",
      "horizon_months": 12,
      "adjuster_count": 1,
      "adjuster_summary": "Expense: +20% Rent from Mar 2026",
      "created_at": "2026-01-20T14:00:00Z",
      "updated_at": "2026-01-20T14:00:00Z",
      "last_run_at": "2026-01-20T14:00:00Z",
      "is_stale": true
    }
  ],
  "total": 2,
  "limit": 50,
  "offset": 0
}
```

**Note:** `is_stale` is `true` when transaction data has changed since `last_run_at`.

---

### 4. Get Scenario

**`GET /api/scenarios/{scenario_id}`**

Retrieve a specific saved scenario with full configuration.

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `scenario_id` | integer | Yes | Scenario ID |

#### Response (200 OK)

```json
{
  "id": 1,
  "name": "Job Loss - June 2026",
  "description": "Scenario modeling complete job loss starting June 2026",
  "horizon_months": 12,
  "starting_balance": 25000.00,
  "adjusters": [
    {
      "id": 1,
      "type": "income_change",
      "category_id": 1,
      "category_name": "Salary",
      "adjustment_type": "percentage",
      "adjustment_value": -100.0,
      "start_date": "2026-06-01",
      "end_date": null
    }
  ],
  "created_at": "2026-01-23T10:30:00Z",
  "updated_at": "2026-01-23T10:30:00Z",
  "last_run_at": "2026-01-23T10:30:00Z",
  "is_stale": false
}
```

#### Error Responses

| Status | Error Code | Description |
|--------|------------|-------------|
| 404 | `SCENARIO_NOT_FOUND` | Scenario does not exist |

---

### 5. Update Scenario

**`PUT /api/scenarios/{scenario_id}`**

Update a saved scenario's configuration.

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `scenario_id` | integer | Yes | Scenario ID |

#### Request Body

All fields are optional. Only provided fields will be updated.

```json
{
  "name": "Job Loss - Updated",
  "description": "Updated description",
  "horizon_months": 18,
  "starting_balance": 30000.00,
  "adjusters": [
    {
      "type": "income_change",
      "category_id": 1,
      "adjustment_type": "percentage",
      "adjustment_value": -50.0,
      "start_date": "2026-06-01",
      "end_date": "2026-12-31"
    }
  ]
}
```

#### Response (200 OK)

```json
{
  "id": 1,
  "name": "Job Loss - Updated",
  "description": "Updated description",
  "horizon_months": 18,
  "starting_balance": 30000.00,
  "adjusters": [
    {
      "id": 2,
      "type": "income_change",
      "category_id": 1,
      "category_name": "Salary",
      "adjustment_type": "percentage",
      "adjustment_value": -50.0,
      "start_date": "2026-06-01",
      "end_date": "2026-12-31"
    }
  ],
  "created_at": "2026-01-23T10:30:00Z",
  "updated_at": "2026-01-23T11:45:00Z",
  "last_run_at": "2026-01-23T10:30:00Z",
  "is_stale": true
}
```

#### Error Responses

| Status | Error Code | Description |
|--------|------------|-------------|
| 400 | `INVALID_ADJUSTER` | Invalid adjuster configuration |
| 400 | `DUPLICATE_NAME` | Another scenario with this name exists |
| 404 | `SCENARIO_NOT_FOUND` | Scenario does not exist |
| 422 | `VALIDATION_ERROR` | Request body validation failed |

---

### 6. Delete Scenario

**`DELETE /api/scenarios/{scenario_id}`**

Delete a saved scenario.

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `scenario_id` | integer | Yes | Scenario ID |

#### Response (200 OK)

```json
{
  "message": "Scenario deleted successfully",
  "id": 1
}
```

#### Error Responses

| Status | Error Code | Description |
|--------|------------|-------------|
| 404 | `SCENARIO_NOT_FOUND` | Scenario does not exist |

---

### 7. Refresh Scenario

**`POST /api/scenarios/{scenario_id}/refresh`**

Re-run a saved scenario with current transaction data.

**Performance Requirement:** < 2 seconds (p95)

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `scenario_id` | integer | Yes | Scenario ID |

#### Request Body

Optional overrides for the refresh calculation.

```json
{
  "starting_balance": 28000.00,
  "horizon_months": 18
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `starting_balance` | number | No | Override starting balance |
| `horizon_months` | integer | No | Override projection horizon |

#### Response (200 OK)

Same format as Preview Scenario response, plus scenario metadata:

```json
{
  "scenario": {
    "id": 1,
    "name": "Job Loss - June 2026",
    "description": "Scenario modeling complete job loss starting June 2026"
  },
  "baseline_series": [...],
  "scenario_series": [...],
  "baseline_metrics": {...},
  "scenario_metrics": {...},
  "deltas": {...},
  "generated_at": "2026-01-23T11:00:00Z",
  "previous_run_at": "2026-01-23T10:30:00Z",
  "data_changed_since_last_run": true
}
```

#### Error Responses

| Status | Error Code | Description |
|--------|------------|-------------|
| 400 | `INSUFFICIENT_HISTORY` | Less than 3 months of transaction history |
| 404 | `SCENARIO_NOT_FOUND` | Scenario does not exist |

---

### 8. Get Scenario Comparison

**`GET /api/scenarios/{scenario_id}/comparison`**

Get detailed baseline vs scenario comparison data optimized for charting.

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `scenario_id` | integer | Yes | Scenario ID |

#### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `refresh` | boolean | No | false | Force recalculation with fresh data |
| `starting_balance` | number | No | saved value | Override starting balance |
| `horizon_months` | integer | No | saved value | Override projection horizon |

#### Response (200 OK)

```json
{
  "scenario": {
    "id": 1,
    "name": "Job Loss - June 2026",
    "description": "Scenario modeling complete job loss starting June 2026",
    "adjusters": [
      {
        "type": "income_change",
        "category_id": 1,
        "category_name": "Salary",
        "adjustment_type": "percentage",
        "adjustment_value": -100.0,
        "start_date": "2026-06-01",
        "end_date": null,
        "display_text": "Salary: -100% starting Jun 1, 2026"
      }
    ]
  },
  "comparison": {
    "chart_data": [
      {
        "date": "2026-02-01",
        "baseline_balance": 26500.00,
        "scenario_balance": 26500.00,
        "baseline_income": 5500.00,
        "scenario_income": 5500.00,
        "baseline_expenses": 4000.00,
        "scenario_expenses": 4000.00
      },
      {
        "date": "2026-06-01",
        "baseline_balance": 32500.00,
        "scenario_balance": 28500.00,
        "baseline_income": 5500.00,
        "scenario_income": 0.00,
        "baseline_expenses": 4000.00,
        "scenario_expenses": 4000.00
      },
      {
        "date": "2026-12-01",
        "baseline_balance": 43000.00,
        "scenario_balance": 4500.00,
        "baseline_income": 5500.00,
        "scenario_income": 0.00,
        "baseline_expenses": 4000.00,
        "scenario_expenses": 4000.00
      }
    ],
    "baseline_metrics": {
      "runway_months": null,
      "min_balance": 25000.00,
      "min_balance_date": "2026-02-01",
      "total_income": 66000.00,
      "total_expenses": 48000.00,
      "total_net_cash_flow": 18000.00,
      "average_monthly_income": 5500.00,
      "average_monthly_expenses": 4000.00,
      "ending_balance": 43000.00
    },
    "scenario_metrics": {
      "runway_months": 7.1,
      "min_balance": 0.00,
      "min_balance_date": "2026-12-15",
      "total_income": 27500.00,
      "total_expenses": 48000.00,
      "total_net_cash_flow": -20500.00,
      "average_monthly_income": 2291.67,
      "average_monthly_expenses": 4000.00,
      "ending_balance": 4500.00
    },
    "deltas": {
      "runway_months_delta": -999,
      "runway_months_display": "N/A → 7.1 months",
      "min_balance_delta": -25000.00,
      "total_income_delta": -38500.00,
      "total_expenses_delta": 0.00,
      "total_net_cash_flow_delta": -38500.00,
      "ending_balance_delta": -38500.00
    },
    "highlights": [
      {
        "type": "warning",
        "message": "Balance reaches $0 on December 15, 2026",
        "date": "2026-12-15"
      },
      {
        "type": "info",
        "message": "Income reduced by $38,500 over 12 months",
        "value": -38500.00
      }
    ]
  },
  "generated_at": "2026-01-23T10:30:00Z",
  "is_stale": false
}
```

#### Error Responses

| Status | Error Code | Description |
|--------|------------|-------------|
| 400 | `INSUFFICIENT_HISTORY` | Less than 3 months of transaction history |
| 404 | `SCENARIO_NOT_FOUND` | Scenario does not exist |

---

## Use Case Examples

### Example 1: Quick Preview - "What if my rent increases?"

**Request:**
```bash
POST /api/scenarios/preview
Content-Type: application/json

{
  "name": "Rent Increase Preview",
  "horizon_months": 12,
  "starting_balance": 15000.00,
  "adjusters": [
    {
      "type": "expense_change",
      "category_id": 5,
      "adjustment_type": "fixed_amount",
      "adjustment_value": 200.00,
      "start_date": "2026-03-01",
      "end_date": null
    }
  ]
}
```

**Response Summary:**
- Baseline runway: unlimited (positive cash flow)
- Scenario runway: unlimited (still positive, but reduced)
- Monthly impact: -$200/month
- Annual impact: -$2,400

---

### Example 2: Save and Monitor - "Job Loss Scenario"

**Step 1: Create Scenario**
```bash
POST /api/scenarios
Content-Type: application/json

{
  "name": "Job Loss - June 2026",
  "description": "Model losing my job and living on savings",
  "horizon_months": 18,
  "starting_balance": 50000.00,
  "adjusters": [
    {
      "type": "income_change",
      "category_id": 1,
      "adjustment_type": "percentage",
      "adjustment_value": -100.0,
      "start_date": "2026-06-01",
      "end_date": null
    }
  ]
}
```

**Step 2: View Comparison Later**
```bash
GET /api/scenarios/1/comparison
```

**Step 3: Refresh After Importing New Transactions**
```bash
POST /api/scenarios/1/refresh
Content-Type: application/json

{
  "starting_balance": 52000.00
}
```

---

### Example 3: Model Expense Increase by Percentage

**Request:**
```bash
POST /api/scenarios/preview
Content-Type: application/json

{
  "name": "20% Rent Increase",
  "horizon_months": 12,
  "starting_balance": 20000.00,
  "adjusters": [
    {
      "type": "expense_change",
      "category_id": 5,
      "adjustment_type": "percentage",
      "adjustment_value": 20.0,
      "start_date": "2026-04-01",
      "end_date": null
    }
  ]
}
```

---

## Database Schema (Reference)

The following tables support scenario persistence:

### scenarios

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY | Unique identifier |
| `name` | VARCHAR(255) | NOT NULL, UNIQUE | Scenario name |
| `description` | TEXT | NULLABLE | Scenario description |
| `horizon_months` | INTEGER | NOT NULL, DEFAULT 12 | Projection horizon |
| `starting_balance` | DECIMAL(12,2) | NOT NULL, DEFAULT 0 | Starting balance |
| `created_at` | TIMESTAMP | NOT NULL | Creation timestamp |
| `updated_at` | TIMESTAMP | NOT NULL | Last update timestamp |
| `last_run_at` | TIMESTAMP | NULLABLE | Last calculation timestamp |

### scenario_adjusters

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY | Unique identifier |
| `scenario_id` | INTEGER | FOREIGN KEY | Parent scenario |
| `type` | VARCHAR(50) | NOT NULL | Adjuster type |
| `category_id` | INTEGER | NULLABLE, FOREIGN KEY | Target category |
| `adjustment_type` | VARCHAR(20) | NOT NULL | percentage or fixed_amount |
| `adjustment_value` | DECIMAL(12,2) | NOT NULL | Adjustment value |
| `start_date` | DATE | NOT NULL | Adjustment start date |
| `end_date` | DATE | NULLABLE | Adjustment end date |

---

## Implementation Notes

### Classification Integration

All scenario calculations must respect the classification system:
- Exclude transactions where `exclude_from_income_calc = true` from income adjustments
- Exclude transactions where `exclude_from_expense_calc = true` from expense adjustments
- Exclude transactions where `is_transfer = true` from all calculations

### Historical Data Requirements

Scenarios require at least 3 months of transaction history to generate accurate baseline projections. If insufficient data exists, return `400 INSUFFICIENT_HISTORY`.

### Staleness Detection

A scenario is considered "stale" when:
- New transactions have been imported since `last_run_at`
- Transaction classifications have changed since `last_run_at`
- Categories referenced by adjusters have been modified

### Performance Considerations

- Preview and refresh operations should complete in < 2 seconds (p95)
- Use the existing ProjectionService for baseline calculations
- Cache category lookups during calculation
- Consider pre-computing monthly aggregates for faster calculations

---

## Related Endpoints

These existing endpoints are used in conjunction with scenario features:

| Endpoint | Description |
|----------|-------------|
| `GET /api/categories` | List categories for adjuster configuration |
| `GET /api/projections/cashflow` | Baseline projection engine |
| `GET /api/analysis/income` | Historical income analysis |
| `GET /api/analysis/expenses` | Historical expense analysis |

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-23 | Engineering | Initial API specification |
