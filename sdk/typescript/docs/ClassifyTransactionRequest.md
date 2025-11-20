
# ClassifyTransactionRequest

Schema for classifying a transaction.

## Properties

Name | Type
------------ | -------------
`classificationId` | number

## Example

```typescript
import type { ClassifyTransactionRequest } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "classificationId": null,
} satisfies ClassifyTransactionRequest

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as ClassifyTransactionRequest
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


