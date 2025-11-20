
# CalculatedBalance

Schema for calculated balance response.

## Properties

Name | Type
------------ | -------------
`accountId` | number
`asOfDate` | Date
`total` | string
`cash` | string
`investments` | string
`basedOnTransactions` | number

## Example

```typescript
import type { CalculatedBalance } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "accountId": null,
  "asOfDate": null,
  "total": null,
  "cash": null,
  "investments": null,
  "basedOnTransactions": null,
} satisfies CalculatedBalance

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as CalculatedBalance
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


