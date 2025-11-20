
# CategorySummary

Category summary in a report.

## Properties

Name | Type
------------ | -------------
`category` | string
`amount` | number
`percentage` | number

## Example

```typescript
import type { CategorySummary } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "category": null,
  "amount": null,
  "percentage": null,
} satisfies CategorySummary

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as CategorySummary
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


