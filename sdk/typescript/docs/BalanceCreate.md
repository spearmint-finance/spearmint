
# BalanceCreate

Schema for creating a balance snapshot.

## Properties

Name | Type
------------ | -------------
`balanceDate` | Date
`totalBalance` | [TotalBalance](TotalBalance.md)
`balanceType` | string
`cashBalance` | [CashBalance](CashBalance.md)
`investmentValue` | [InvestmentValue](InvestmentValue.md)
`notes` | string

## Example

```typescript
import type { BalanceCreate } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "balanceDate": null,
  "totalBalance": null,
  "balanceType": null,
  "cashBalance": null,
  "investmentValue": null,
  "notes": null,
} satisfies BalanceCreate

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as BalanceCreate
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


