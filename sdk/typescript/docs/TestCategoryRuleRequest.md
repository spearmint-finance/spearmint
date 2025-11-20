
# TestCategoryRuleRequest

Schema for testing a category rule.

## Properties

Name | Type
------------ | -------------
`descriptionPattern` | string
`sourcePattern` | string
`amountMin` | number
`amountMax` | number
`paymentMethodPattern` | string
`transactionTypePattern` | string
`limit` | number

## Example

```typescript
import type { TestCategoryRuleRequest } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "descriptionPattern": null,
  "sourcePattern": null,
  "amountMin": null,
  "amountMax": null,
  "paymentMethodPattern": null,
  "transactionTypePattern": null,
  "limit": null,
} satisfies TestCategoryRuleRequest

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as TestCategoryRuleRequest
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


