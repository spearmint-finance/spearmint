
# CategoryBreakdown

Category breakdown data.

## Properties

Name | Type
------------ | -------------
`total` | string
`count` | number
`average` | string
`percentage` | number

## Example

```typescript
import type { CategoryBreakdown } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "total": null,
  "count": null,
  "average": null,
  "percentage": null,
} satisfies CategoryBreakdown

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as CategoryBreakdown
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


