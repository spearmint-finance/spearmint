
# RelatedTransactionsResponse

Response with related transactions.

## Properties

Name | Type
------------ | -------------
`transactionId` | number
`relatedTransactions` | [Array&lt;RelatedTransactionInfo&gt;](RelatedTransactionInfo.md)
`count` | number

## Example

```typescript
import type { RelatedTransactionsResponse } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "transactionId": null,
  "relatedTransactions": null,
  "count": null,
} satisfies RelatedTransactionsResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as RelatedTransactionsResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


