
# CreditCardPairsResponse

Response with detected credit card pairs.

## Properties

Name | Type
------------ | -------------
`count` | number
`highConfidence` | number
`pairs` | [Array&lt;CreditCardPairDetection&gt;](CreditCardPairDetection.md)

## Example

```typescript
import type { CreditCardPairsResponse } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "count": null,
  "highConfidence": null,
  "pairs": null,
} satisfies CreditCardPairsResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as CreditCardPairsResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


