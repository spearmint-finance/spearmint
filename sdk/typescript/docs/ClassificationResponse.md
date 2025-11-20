
# ClassificationResponse

Schema for classification response.

## Properties

Name | Type
------------ | -------------
`classificationName` | string
`classificationCode` | string
`description` | string
`excludeFromIncomeCalc` | boolean
`excludeFromExpenseCalc` | boolean
`excludeFromCashflowCalc` | boolean
`classificationId` | number
`isSystemClassification` | boolean
`createdAt` | Date
`updatedAt` | Date

## Example

```typescript
import type { ClassificationResponse } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "classificationName": null,
  "classificationCode": null,
  "description": null,
  "excludeFromIncomeCalc": null,
  "excludeFromExpenseCalc": null,
  "excludeFromCashflowCalc": null,
  "classificationId": null,
  "isSystemClassification": null,
  "createdAt": null,
  "updatedAt": null,
} satisfies ClassificationResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as ClassificationResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


