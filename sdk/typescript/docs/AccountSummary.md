
# AccountSummary

Schema for account summary with balance.

## Properties

Name | Type
------------ | -------------
`accountId` | number
`accountName` | string
`accountType` | string
`institution` | string
`currentBalance` | string
`balanceDate` | Date
`hasCash` | boolean
`hasInvestments` | boolean
`cashBalance` | string
`investmentValue` | string

## Example

```typescript
import type { AccountSummary } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "accountId": null,
  "accountName": null,
  "accountType": null,
  "institution": null,
  "currentBalance": null,
  "balanceDate": null,
  "hasCash": null,
  "hasInvestments": null,
  "cashBalance": null,
  "investmentValue": null,
} satisfies AccountSummary

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as AccountSummary
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


