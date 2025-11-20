
# TransactionSplitRead

Read model for a transaction split.

## Properties

Name | Type
------------ | -------------
`splitId` | number
`transactionId` | number
`personId` | number
`amount` | string
`createdAt` | Date

## Example

```typescript
import type { TransactionSplitRead } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "splitId": null,
  "transactionId": null,
  "personId": null,
  "amount": null,
  "createdAt": null,
} satisfies TransactionSplitRead

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as TransactionSplitRead
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


