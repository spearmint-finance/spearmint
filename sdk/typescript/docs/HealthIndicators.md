
# HealthIndicators

Financial health indicators.

## Properties

Name | Type
------------ | -------------
`incomeToExpenseRatio` | number
`savingsRate` | number
`averageDailyIncome` | number
`averageDailyExpense` | number
`averageDailyCashflow` | number

## Example

```typescript
import type { HealthIndicators } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "incomeToExpenseRatio": null,
  "savingsRate": null,
  "averageDailyIncome": null,
  "averageDailyExpense": null,
  "averageDailyCashflow": null,
} satisfies HealthIndicators

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as HealthIndicators
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


