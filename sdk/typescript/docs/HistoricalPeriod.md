
# HistoricalPeriod

Historical period information.

## Properties

Name | Type
------------ | -------------
`startDate` | string
`endDate` | string
`days` | number
`totalIncome` | number
`totalExpenses` | number
`averageDaily` | number

## Example

```typescript
import type { HistoricalPeriod } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "startDate": null,
  "endDate": null,
  "days": null,
  "totalIncome": null,
  "totalExpenses": null,
  "averageDaily": null,
} satisfies HistoricalPeriod

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as HistoricalPeriod
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


