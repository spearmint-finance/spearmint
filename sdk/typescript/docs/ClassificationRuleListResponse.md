
# ClassificationRuleListResponse

Schema for list of classification rules.

## Properties

Name | Type
------------ | -------------
`rules` | [Array&lt;ClassificationRuleResponse&gt;](ClassificationRuleResponse.md)
`total` | number

## Example

```typescript
import type { ClassificationRuleListResponse } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "rules": null,
  "total": null,
} satisfies ClassificationRuleListResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as ClassificationRuleListResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


