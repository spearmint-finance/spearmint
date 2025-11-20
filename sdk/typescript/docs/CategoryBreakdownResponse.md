
# CategoryBreakdownResponse

Response for category breakdown analysis.

## Properties

Name | Type
------------ | -------------
`incomeCategories` | [Array&lt;CategoryBreakdownItem&gt;](CategoryBreakdownItem.md)
`expenseCategories` | [Array&lt;CategoryBreakdownItem&gt;](CategoryBreakdownItem.md)
`totalIncome` | string
`totalExpenses` | string
`periodStart` | Date
`periodEnd` | Date
`mode` | [AnalysisModeEnumOutput](AnalysisModeEnumOutput.md)

## Example

```typescript
import type { CategoryBreakdownResponse } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "incomeCategories": null,
  "expenseCategories": null,
  "totalIncome": null,
  "totalExpenses": null,
  "periodStart": null,
  "periodEnd": null,
  "mode": null,
} satisfies CategoryBreakdownResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as CategoryBreakdownResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


