
# ReconciliationResponse

Schema for reconciliation responses.

## Properties

Name | Type
------------ | -------------
`reconciliationId` | number
`accountId` | number
`statementDate` | Date
`statementBalance` | string
`calculatedBalance` | string
`statementCashBalance` | string
`calculatedCashBalance` | string
`statementInvestmentValue` | string
`calculatedInvestmentValue` | string
`discrepancyAmount` | string
`isReconciled` | boolean
`reconciledAt` | Date
`reconciledBy` | string
`transactionsClearedCount` | number
`transactionsPendingCount` | number
`notes` | string
`createdAt` | Date
`updatedAt` | Date

## Example

```typescript
import type { ReconciliationResponse } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "reconciliationId": null,
  "accountId": null,
  "statementDate": null,
  "statementBalance": null,
  "calculatedBalance": null,
  "statementCashBalance": null,
  "calculatedCashBalance": null,
  "statementInvestmentValue": null,
  "calculatedInvestmentValue": null,
  "discrepancyAmount": null,
  "isReconciled": null,
  "reconciledAt": null,
  "reconciledBy": null,
  "transactionsClearedCount": null,
  "transactionsPendingCount": null,
  "notes": null,
  "createdAt": null,
  "updatedAt": null,
} satisfies ReconciliationResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as ReconciliationResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


