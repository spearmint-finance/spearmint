
# FinancialHealthResponse

Response for financial health indicators.

## Properties

Name | Type
------------ | -------------
`incomeToExpenseRatio` | number
`savingsRate` | number
`averageDailyIncome` | string
`averageDailyExpense` | string
`netDailyCashFlow` | string
`periodStart` | Date
`periodEnd` | Date

## Example

```typescript
import type { FinancialHealthResponse } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "incomeToExpenseRatio": null,
  "savingsRate": null,
  "averageDailyIncome": null,
  "averageDailyExpense": null,
  "netDailyCashFlow": null,
  "periodStart": null,
  "periodEnd": null,
} satisfies FinancialHealthResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as FinancialHealthResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


