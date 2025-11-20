
# TransactionClearRequest

Schema for clearing transactions.

## Properties

Name | Type
------------ | -------------
`transactionIds` | Array&lt;number&gt;
`clearedDate` | Date

## Example

```typescript
import type { TransactionClearRequest } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "transactionIds": null,
  "clearedDate": null,
} satisfies TransactionClearRequest

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as TransactionClearRequest
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


