
# AccountUpdate

Schema for updating an account.

## Properties

Name | Type
------------ | -------------
`accountName` | string
`accountSubtype` | string
`institutionName` | string
`accountNumberLast4` | string
`isActive` | boolean
`notes` | string

## Example

```typescript
import type { AccountUpdate } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "accountName": null,
  "accountSubtype": null,
  "institutionName": null,
  "accountNumberLast4": null,
  "isActive": null,
  "notes": null,
} satisfies AccountUpdate

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as AccountUpdate
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


