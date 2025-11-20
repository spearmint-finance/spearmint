
# ApplyCategoryRulesRequest

Schema for applying category rules.

## Properties

Name | Type
------------ | -------------
`transactionIds` | Array&lt;number&gt;
`ruleIds` | Array&lt;number&gt;
`forceRecategorize` | boolean

## Example

```typescript
import type { ApplyCategoryRulesRequest } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "transactionIds": null,
  "ruleIds": null,
  "forceRecategorize": null,
} satisfies ApplyCategoryRulesRequest

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as ApplyCategoryRulesRequest
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


