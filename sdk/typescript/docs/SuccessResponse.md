
# SuccessResponse

Success response schema.

## Properties

Name | Type
------------ | -------------
`message` | string
`data` | { [key: string]: any; }

## Example

```typescript
import type { SuccessResponse } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "message": null,
  "data": null,
} satisfies SuccessResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as SuccessResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


