
# CashflowProjectionResponse

Response for cash flow projections.

## Properties

Name | Type
------------ | -------------
`projectionType` | string
`historicalPeriod` | [HistoricalPeriod](HistoricalPeriod.md)
`projectionPeriod` | [ProjectionPeriod](ProjectionPeriod.md)
`method` | string
`confidenceLevel` | number
`projectedIncome` | number
`projectedExpenses` | number
`projectedCashflow` | number
`confidenceInterval` | [ConfidenceInterval](ConfidenceInterval.md)
`dailyProjections` | [Array&lt;CashflowDailyProjection&gt;](CashflowDailyProjection.md)
`scenarios` | [Scenarios](Scenarios.md)

## Example

```typescript
import type { CashflowProjectionResponse } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "projectionType": null,
  "historicalPeriod": null,
  "projectionPeriod": null,
  "method": null,
  "confidenceLevel": null,
  "projectedIncome": null,
  "projectedExpenses": null,
  "projectedCashflow": null,
  "confidenceInterval": null,
  "dailyProjections": null,
  "scenarios": null,
} satisfies CashflowProjectionResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as CashflowProjectionResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


