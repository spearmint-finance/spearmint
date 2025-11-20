
# ApplyRulesRequest

Schema for applying classification rules.

## Properties

Name | Type
------------ | -------------
`dryRun` | boolean
`ruleIds` | Array&lt;number&gt;

## Example

```typescript
import type { ApplyRulesRequest } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "dryRun": null,
  "ruleIds": null,
} satisfies ApplyRulesRequest

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as ApplyRulesRequest
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


