
# CashFlowResponse

Response for cash flow analysis.

## Properties

Name | Type
------------ | -------------
`netCashFlow` | string
`totalIncome` | string
`totalExpenses` | string
`incomeCount` | number
`expenseCount` | number
`periodStart` | Date
`periodEnd` | Date
`mode` | [AnalysisModeEnumOutput](AnalysisModeEnumOutput.md)

## Example

```typescript
import type { CashFlowResponse } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "netCashFlow": null,
  "totalIncome": null,
  "totalExpenses": null,
  "incomeCount": null,
  "expenseCount": null,
  "periodStart": null,
  "periodEnd": null,
  "mode": null,
} satisfies CashFlowResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as CashFlowResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


