
# CategoryRuleResponse

Schema for category rule response.

## Properties

Name | Type
------------ | -------------
`ruleName` | string
`rulePriority` | number
`categoryId` | number
`isActive` | boolean
`descriptionPattern` | string
`sourcePattern` | string
`amountMin` | number
`amountMax` | number
`paymentMethodPattern` | string
`transactionTypePattern` | string
`ruleId` | number
`createdAt` | Date
`updatedAt` | Date

## Example

```typescript
import type { CategoryRuleResponse } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "ruleName": null,
  "rulePriority": null,
  "categoryId": null,
  "isActive": null,
  "descriptionPattern": null,
  "sourcePattern": null,
  "amountMin": null,
  "amountMax": null,
  "paymentMethodPattern": null,
  "transactionTypePattern": null,
  "ruleId": null,
  "createdAt": null,
  "updatedAt": null,
} satisfies CategoryRuleResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as CategoryRuleResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


