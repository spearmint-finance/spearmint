
# ExpenseSummary

Expense summary in a report.

## Properties

Name | Type
------------ | -------------
`total` | number
`transactionCount` | number
`averageTransaction` | number
`topCategories` | [Array&lt;CategorySummary&gt;](CategorySummary.md)

## Example

```typescript
import type { ExpenseSummary } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "total": null,
  "transactionCount": null,
  "averageTransaction": null,
  "topCategories": null,
} satisfies ExpenseSummary

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as ExpenseSummary
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


