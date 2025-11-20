
# CategoryRuleCreate

Schema for creating a category rule.

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

## Example

```typescript
import type { CategoryRuleCreate } from '@spearmint-money/sdk'

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
} satisfies CategoryRuleCreate

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as CategoryRuleCreate
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


