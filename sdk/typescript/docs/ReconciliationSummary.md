
# ReconciliationSummary

Summary for reconciliation report.

## Properties

Name | Type
------------ | -------------
`totalIncome` | number
`totalExpenses` | number
`netCashflow` | number
`transactionCount` | number

## Example

```typescript
import type { ReconciliationSummary } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "totalIncome": null,
  "totalExpenses": null,
  "netCashflow": null,
  "transactionCount": null,
} satisfies ReconciliationSummary

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as ReconciliationSummary
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


