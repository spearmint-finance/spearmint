
# ImportResponse

Schema for import response.

## Properties

Name | Type
------------ | -------------
`totalRows` | number
`successfulRows` | number
`failedRows` | number
`classifiedRows` | number
`skippedDuplicates` | number
`successRate` | number
`errors` | [Array&lt;ImportErrorDetail&gt;](ImportErrorDetail.md)
`warnings` | Array&lt;string&gt;

## Example

```typescript
import type { ImportResponse } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "totalRows": null,
  "successfulRows": null,
  "failedRows": null,
  "classifiedRows": null,
  "skippedDuplicates": null,
  "successRate": null,
  "errors": null,
  "warnings": null,
} satisfies ImportResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as ImportResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


