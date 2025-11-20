
# CashflowDailyProjection

Daily cash flow projection data point.

## Properties

Name | Type
------------ | -------------
`date` | string
`projectedIncome` | number
`projectedExpenses` | number
`projectedCashflow` | number
`cashflowLower` | number
`cashflowUpper` | number

## Example

```typescript
import type { CashflowDailyProjection } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "date": null,
  "projectedIncome": null,
  "projectedExpenses": null,
  "projectedCashflow": null,
  "cashflowLower": null,
  "cashflowUpper": null,
} satisfies CashflowDailyProjection

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as CashflowDailyProjection
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


