
# PortfolioSummary

Schema for portfolio summary.

## Properties

Name | Type
------------ | -------------
`accountId` | number
`accountName` | string
`totalValue` | string
`totalCostBasis` | string
`totalGainLoss` | string
`holdings` | [Array&lt;HoldingResponse&gt;](HoldingResponse.md)
`asOfDate` | Date

## Example

```typescript
import type { PortfolioSummary } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "accountId": null,
  "accountName": null,
  "totalValue": null,
  "totalCostBasis": null,
  "totalGainLoss": null,
  "holdings": null,
  "asOfDate": null,
} satisfies PortfolioSummary

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as PortfolioSummary
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


