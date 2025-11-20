
# AccountCreate

Schema for creating a new account.

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
`openingBalance` | [OpeningBalance](OpeningBalance.md)
`openingBalanceDate` | Date

## Example

```typescript
import type { AccountCreate } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "accountName": null,
  "accountType": null,
  "accountSubtype": null,
  "institutionName": null,
  "accountNumberLast4": null,
  "currency": null,
  "notes": null,
  "openingBalance": null,
  "openingBalanceDate": null,
} satisfies AccountCreate

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as AccountCreate
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


