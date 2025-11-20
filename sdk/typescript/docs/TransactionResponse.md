
# TransactionResponse

Schema for transaction response.

## Properties

Name | Type
------------ | -------------
`transactionDate` | Date
`amount` | string
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
`transactionId` | number
`relatedTransactionId` | number
`category` | [CategoryInfo](CategoryInfo.md)
`classification` | [ClassificationInfo](ClassificationInfo.md)
`tags` | [Array&lt;TagInfo&gt;](TagInfo.md)
`createdAt` | Date
`updatedAt` | Date

## Example

```typescript
import type { TransactionResponse } from '@spearmint-money/sdk'

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
  "transactionId": null,
  "relatedTransactionId": null,
  "category": null,
  "classification": null,
  "tags": null,
  "createdAt": null,
  "updatedAt": null,
} satisfies TransactionResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as TransactionResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


