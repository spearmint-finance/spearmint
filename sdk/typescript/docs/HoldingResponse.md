
# HoldingResponse

Schema for holding responses.

## Properties

Name | Type
------------ | -------------
`holdingId` | number
`accountId` | number
`symbol` | string
`description` | string
`quantity` | string
`costBasis` | string
`currentValue` | string
`asOfDate` | Date
`assetClass` | string
`sector` | string
`createdAt` | Date
`updatedAt` | Date
`gainLoss` | string
`gainLossPercent` | number

## Example

```typescript
import type { HoldingResponse } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "holdingId": null,
  "accountId": null,
  "symbol": null,
  "description": null,
  "quantity": null,
  "costBasis": null,
  "currentValue": null,
  "asOfDate": null,
  "assetClass": null,
  "sector": null,
  "createdAt": null,
  "updatedAt": null,
  "gainLoss": null,
  "gainLossPercent": null,
} satisfies HoldingResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as HoldingResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


