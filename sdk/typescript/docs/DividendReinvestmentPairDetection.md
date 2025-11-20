
# DividendReinvestmentPairDetection

Detected dividend reinvestment pair.

## Properties

Name | Type
------------ | -------------
`dividend` | [TransactionSummary](TransactionSummary.md)
`reinvestment` | [TransactionSummary](TransactionSummary.md)
`confidence` | number
`amountDifference` | string
`dateDifferenceDays` | number
`relationshipType` | string

## Example

```typescript
import type { DividendReinvestmentPairDetection } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "dividend": null,
  "reinvestment": null,
  "confidence": null,
  "amountDifference": null,
  "dateDifferenceDays": null,
  "relationshipType": null,
} satisfies DividendReinvestmentPairDetection

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as DividendReinvestmentPairDetection
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


