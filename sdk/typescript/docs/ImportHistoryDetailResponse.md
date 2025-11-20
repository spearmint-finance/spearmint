
# ImportHistoryDetailResponse

Schema for detailed import history response.

## Properties

Name | Type
------------ | -------------
`importId` | number
`importDate` | Date
`fileName` | string
`filePath` | string
`totalRows` | number
`successfulRows` | number
`failedRows` | number
`classifiedRows` | number
`importMode` | string
`errorLog` | string
`successRate` | number

## Example

```typescript
import type { ImportHistoryDetailResponse } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "importId": null,
  "importDate": null,
  "fileName": null,
  "filePath": null,
  "totalRows": null,
  "successfulRows": null,
  "failedRows": null,
  "classifiedRows": null,
  "importMode": null,
  "errorLog": null,
  "successRate": null,
} satisfies ImportHistoryDetailResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as ImportHistoryDetailResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


