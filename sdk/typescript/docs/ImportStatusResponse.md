
# ImportStatusResponse

Schema for import status response.

## Properties

Name | Type
------------ | -------------
`importId` | number
`status` | string
`progress` | number
`currentRow` | number
`totalRows` | number
`successfulRows` | number
`failedRows` | number
`message` | string
`startedAt` | Date
`completedAt` | Date

## Example

```typescript
import type { ImportStatusResponse } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "importId": null,
  "status": null,
  "progress": null,
  "currentRow": null,
  "totalRows": null,
  "successfulRows": null,
  "failedRows": null,
  "message": null,
  "startedAt": null,
  "completedAt": null,
} satisfies ImportStatusResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as ImportStatusResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


