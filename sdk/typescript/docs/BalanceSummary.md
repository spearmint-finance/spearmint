
# BalanceSummary

High-level balance summary.

## Properties

Name | Type
------------ | -------------
`totalAssets` | number
`totalLiabilities` | number
`netWorth` | number

## Example

```typescript
import type { BalanceSummary } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "totalAssets": null,
  "totalLiabilities": null,
  "netWorth": null,
} satisfies BalanceSummary

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as BalanceSummary
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


