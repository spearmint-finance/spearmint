
# TestRuleResponse

Schema for rule test response.

## Properties

Name | Type
------------ | -------------
`matchingTransactions` | number
`sampleTransactionIds` | Array&lt;number&gt;

## Example

```typescript
import type { TestRuleResponse } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "matchingTransactions": null,
  "sampleTransactionIds": null,
} satisfies TestRuleResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as TestRuleResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


