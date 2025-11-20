
# FixResult


## Properties

Name | Type
------------ | -------------
`taskName` | string
`status` | string
`details` | { [key: string]: any; }
`rowsAffected` | number

## Example

```typescript
import type { FixResult } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "taskName": null,
  "status": null,
  "details": null,
  "rowsAffected": null,
} satisfies FixResult

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as FixResult
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


