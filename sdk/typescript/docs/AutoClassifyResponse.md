
# AutoClassifyResponse

Schema for auto-classification response.

## Properties

Name | Type
------------ | -------------
`totalProcessed` | number
`classifiedCount` | number
`skippedCount` | number

## Example

```typescript
import type { AutoClassifyResponse } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "totalProcessed": null,
  "classifiedCount": null,
  "skippedCount": null,
} satisfies AutoClassifyResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as AutoClassifyResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


