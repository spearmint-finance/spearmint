
# BalanceHistory

Schema for balance history response.

## Properties

Name | Type
------------ | -------------
`accountId` | number
`accountName` | string
`balances` | [Array&lt;BalanceResponse&gt;](BalanceResponse.md)
`startDate` | Date
`endDate` | Date

## Example

```typescript
import type { BalanceHistory } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "accountId": null,
  "accountName": null,
  "balances": null,
  "startDate": null,
  "endDate": null,
} satisfies BalanceHistory

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as BalanceHistory
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


