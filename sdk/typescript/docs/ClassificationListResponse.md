
# ClassificationListResponse

Schema for list of classifications.

## Properties

Name | Type
------------ | -------------
`classifications` | [Array&lt;ClassificationResponse&gt;](ClassificationResponse.md)
`total` | number

## Example

```typescript
import type { ClassificationListResponse } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "classifications": null,
  "total": null,
} satisfies ClassificationListResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as ClassificationListResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


