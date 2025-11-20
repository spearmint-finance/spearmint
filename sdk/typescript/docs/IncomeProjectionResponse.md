
# IncomeProjectionResponse

Response for income projections.

## Properties

Name | Type
------------ | -------------
`projectionType` | string
`historicalPeriod` | [HistoricalPeriod](HistoricalPeriod.md)
`projectionPeriod` | [ProjectionPeriod](ProjectionPeriod.md)
`method` | string
`confidenceLevel` | number
`projectedTotal` | number
`confidenceInterval` | [ConfidenceInterval](ConfidenceInterval.md)
`dailyProjections` | [Array&lt;DailyProjection&gt;](DailyProjection.md)
`modelMetrics` | [ModelMetrics](ModelMetrics.md)

## Example

```typescript
import type { IncomeProjectionResponse } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "projectionType": null,
  "historicalPeriod": null,
  "projectionPeriod": null,
  "method": null,
  "confidenceLevel": null,
  "projectedTotal": null,
  "confidenceInterval": null,
  "dailyProjections": null,
  "modelMetrics": null,
} satisfies IncomeProjectionResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as IncomeProjectionResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


