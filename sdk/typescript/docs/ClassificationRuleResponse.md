
# ClassificationRuleResponse

Schema for classification rule response.

## Properties

Name | Type
------------ | -------------
`ruleName` | string
`rulePriority` | number
`classificationId` | number
`isActive` | boolean
`descriptionPattern` | string
`categoryPattern` | string
`sourcePattern` | string
`amountMin` | number
`amountMax` | number
`paymentMethodPattern` | string
`ruleId` | number
`createdAt` | Date
`updatedAt` | Date

## Example

```typescript
import type { ClassificationRuleResponse } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "ruleName": null,
  "rulePriority": null,
  "classificationId": null,
  "isActive": null,
  "descriptionPattern": null,
  "categoryPattern": null,
  "sourcePattern": null,
  "amountMin": null,
  "amountMax": null,
  "paymentMethodPattern": null,
  "ruleId": null,
  "createdAt": null,
  "updatedAt": null,
} satisfies ClassificationRuleResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as ClassificationRuleResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


