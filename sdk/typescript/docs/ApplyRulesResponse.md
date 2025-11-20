
# ApplyRulesResponse

Schema for apply rules response.

## Properties

Name | Type
------------ | -------------
`dryRun` | boolean
`totalRulesProcessed` | number
`totalTransactionsUpdated` | number
`rulesApplied` | Array&lt;{ [key: string]: any; }&gt;

## Example

```typescript
import type { ApplyRulesResponse } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "dryRun": null,
  "totalRulesProcessed": null,
  "totalTransactionsUpdated": null,
  "rulesApplied": null,
} satisfies ApplyRulesResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as ApplyRulesResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


