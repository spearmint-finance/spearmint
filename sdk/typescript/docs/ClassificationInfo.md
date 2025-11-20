
# ClassificationInfo

Classification information for transaction response.

## Properties

Name | Type
------------ | -------------
`classificationId` | number
`classificationName` | string
`classificationCode` | string

## Example

```typescript
import type { ClassificationInfo } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "classificationId": null,
  "classificationName": null,
  "classificationCode": null,
} satisfies ClassificationInfo

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as ClassificationInfo
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


