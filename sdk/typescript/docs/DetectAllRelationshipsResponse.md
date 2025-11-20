
# DetectAllRelationshipsResponse

Response with all detected relationships.

## Properties

Name | Type
------------ | -------------
`transferPairs` | [TransferPairsResponse](TransferPairsResponse.md)
`creditCardPairs` | [CreditCardPairsResponse](CreditCardPairsResponse.md)
`reimbursementPairs` | [ReimbursementPairsResponse](ReimbursementPairsResponse.md)
`dividendReinvestmentPairs` | [DividendReinvestmentPairsResponse](DividendReinvestmentPairsResponse.md)
`totalDetected` | number
`autoLinked` | boolean

## Example

```typescript
import type { DetectAllRelationshipsResponse } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "transferPairs": null,
  "creditCardPairs": null,
  "reimbursementPairs": null,
  "dividendReinvestmentPairs": null,
  "totalDetected": null,
  "autoLinked": null,
} satisfies DetectAllRelationshipsResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as DetectAllRelationshipsResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


