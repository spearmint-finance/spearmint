
# ApplyCategoryRulesResponse

Schema for apply category rules response.

## Properties

Name | Type
------------ | -------------
`totalProcessed` | number
`categorizedCount` | number
`skippedCount` | number
`rulesApplied` | number

## Example

```typescript
import type { ApplyCategoryRulesResponse } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "totalProcessed": null,
  "categorizedCount": null,
  "skippedCount": null,
  "rulesApplied": null,
} satisfies ApplyCategoryRulesResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as ApplyCategoryRulesResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


