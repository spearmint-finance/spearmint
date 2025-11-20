
# CategoryRuleListResponse

Schema for category rule list response.

## Properties

Name | Type
------------ | -------------
`rules` | [Array&lt;CategoryRuleResponse&gt;](CategoryRuleResponse.md)
`total` | number

## Example

```typescript
import type { CategoryRuleListResponse } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "rules": null,
  "total": null,
} satisfies CategoryRuleListResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as CategoryRuleListResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


