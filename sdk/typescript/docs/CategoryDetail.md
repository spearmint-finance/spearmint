
# CategoryDetail

Detailed category information.

## Properties

Name | Type
------------ | -------------
`category` | string
`total` | number
`count` | number
`average` | number
`percentage` | number

## Example

```typescript
import type { CategoryDetail } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "category": null,
  "total": null,
  "count": null,
  "average": null,
  "percentage": null,
} satisfies CategoryDetail

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as CategoryDetail
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


