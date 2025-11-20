
# ExpenseAnalysisResponse

Response for expense analysis.

## Properties

Name | Type
------------ | -------------
`totalExpenses` | string
`transactionCount` | number
`averageTransaction` | string
`breakdownByCategory` | [{ [key: string]: CategoryBreakdown; }](CategoryBreakdown.md)
`topCategories` | [Array&lt;TopCategory&gt;](TopCategory.md)
`periodStart` | Date
`periodEnd` | Date
`mode` | [AnalysisModeEnumOutput](AnalysisModeEnumOutput.md)

## Example

```typescript
import type { ExpenseAnalysisResponse } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "totalExpenses": null,
  "transactionCount": null,
  "averageTransaction": null,
  "breakdownByCategory": null,
  "topCategories": null,
  "periodStart": null,
  "periodEnd": null,
  "mode": null,
} satisfies ExpenseAnalysisResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as ExpenseAnalysisResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


