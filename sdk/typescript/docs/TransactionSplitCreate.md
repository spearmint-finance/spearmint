
# TransactionSplitCreate

Create a split for a transaction.

## Properties

Name | Type
------------ | -------------
`personId` | number
`amount` | [Amount1](Amount1.md)

## Example

```typescript
import type { TransactionSplitCreate } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "personId": null,
  "amount": null,
} satisfies TransactionSplitCreate

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as TransactionSplitCreate
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


