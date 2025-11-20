
# RelatedTransactionInfo

Information about a related transaction.

## Properties

Name | Type
------------ | -------------
`transaction` | [TransactionSummary](TransactionSummary.md)
`relationshipType` | string
`relationshipDescription` | string

## Example

```typescript
import type { RelatedTransactionInfo } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "transaction": null,
  "relationshipType": null,
  "relationshipDescription": null,
} satisfies RelatedTransactionInfo

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as RelatedTransactionInfo
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


