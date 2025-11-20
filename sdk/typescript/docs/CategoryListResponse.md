
# CategoryListResponse

Schema for category list response.

## Properties

Name | Type
------------ | -------------
`categories` | [Array&lt;CategoryResponse&gt;](CategoryResponse.md)
`total` | number

## Example

```typescript
import type { CategoryListResponse } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "categories": null,
  "total": null,
} satisfies CategoryListResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as CategoryListResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


