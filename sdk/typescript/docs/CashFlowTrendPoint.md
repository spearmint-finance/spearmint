
# CashFlowTrendPoint

Cash flow trend data point.

## Properties

Name | Type
------------ | -------------
`period` | string
`income` | string
`expenses` | string
`netCashFlow` | string
`incomeCount` | number
`expenseCount` | number

## Example

```typescript
import type { CashFlowTrendPoint } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "period": null,
  "income": null,
  "expenses": null,
  "netCashFlow": null,
  "incomeCount": null,
  "expenseCount": null,
} satisfies CashFlowTrendPoint

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as CashFlowTrendPoint
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


