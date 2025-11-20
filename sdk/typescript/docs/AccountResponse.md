
# AccountResponse

Schema for account responses.

## Properties

Name | Type
------------ | -------------
`accountName` | string
`accountType` | string
`accountSubtype` | string
`institutionName` | string
`accountNumberLast4` | string
`currency` | string
`notes` | string
`accountId` | number
`isActive` | boolean
`hasCashComponent` | boolean
`hasInvestmentComponent` | boolean
`openingBalance` | string
`openingBalanceDate` | Date
`createdAt` | Date
`updatedAt` | Date
`currentBalance` | string
`currentBalanceDate` | Date
`cashBalance` | string
`investmentValue` | string

## Example

```typescript
import type { AccountResponse } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "accountName": null,
  "accountType": null,
  "accountSubtype": null,
  "institutionName": null,
  "accountNumberLast4": null,
  "currency": null,
  "notes": null,
  "accountId": null,
  "isActive": null,
  "hasCashComponent": null,
  "hasInvestmentComponent": null,
  "openingBalance": null,
  "openingBalanceDate": null,
  "createdAt": null,
  "updatedAt": null,
  "currentBalance": null,
  "currentBalanceDate": null,
  "cashBalance": null,
  "investmentValue": null,
} satisfies AccountResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as AccountResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


