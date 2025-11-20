
# ImportErrorDetail

Schema for import error detail.

## Properties

Name | Type
------------ | -------------
`row` | number
`field` | string
`message` | string
`value` | [](.md)

## Example

```typescript
import type { ImportErrorDetail } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "row": null,
  "field": null,
  "message": null,
  "value": null,
} satisfies ImportErrorDetail

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as ImportErrorDetail
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


