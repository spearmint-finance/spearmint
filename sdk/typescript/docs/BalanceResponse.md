
# BalanceResponse

Schema for balance responses.

## Properties

Name | Type
------------ | -------------
`balanceId` | number
`accountId` | number
`balanceDate` | Date
`totalBalance` | string
`balanceType` | string
`cashBalance` | string
`investmentValue` | string
`notes` | string
`createdAt` | Date
`updatedAt` | Date

## Example

```typescript
import type { BalanceResponse } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "balanceId": null,
  "accountId": null,
  "balanceDate": null,
  "totalBalance": null,
  "balanceType": null,
  "cashBalance": null,
  "investmentValue": null,
  "notes": null,
  "createdAt": null,
  "updatedAt": null,
} satisfies BalanceResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as BalanceResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


