
# TransactionUpdate

Schema for updating a transaction.

## Properties

Name | Type
------------ | -------------
`transactionDate` | Date
`amount` | [Amount2](Amount2.md)
`transactionType` | string
`categoryId` | number
`source` | string
`description` | string
`paymentMethod` | string
`classificationId` | number
`includeInAnalysis` | boolean
`isTransfer` | boolean
`transferAccountFrom` | string
`transferAccountTo` | string
`notes` | string
`tagNames` | Array&lt;string&gt;
`reapplyRules` | boolean

## Example

```typescript
import type { TransactionUpdate } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "transactionDate": null,
  "amount": null,
  "transactionType": null,
  "categoryId": null,
  "source": null,
  "description": null,
  "paymentMethod": null,
  "classificationId": null,
  "includeInAnalysis": null,
  "isTransfer": null,
  "transferAccountFrom": null,
  "transferAccountTo": null,
  "notes": null,
  "tagNames": null,
  "reapplyRules": null,
} satisfies TransactionUpdate

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as TransactionUpdate
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


