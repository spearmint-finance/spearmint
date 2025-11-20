
# PersonRead

Schema returned for a person.

## Properties

Name | Type
------------ | -------------
`personId` | number
`name` | string
`isActive` | boolean
`createdAt` | Date

## Example

```typescript
import type { PersonRead } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "personId": null,
  "name": null,
  "isActive": null,
  "createdAt": null,
} satisfies PersonRead

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as PersonRead
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


