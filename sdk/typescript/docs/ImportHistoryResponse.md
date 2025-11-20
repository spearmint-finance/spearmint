
# ImportHistoryResponse

Schema for import history list response.

## Properties

Name | Type
------------ | -------------
`imports` | [Array&lt;ImportHistoryItem&gt;](ImportHistoryItem.md)
`total` | number

## Example

```typescript
import type { ImportHistoryResponse } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "imports": null,
  "total": null,
} satisfies ImportHistoryResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as ImportHistoryResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


