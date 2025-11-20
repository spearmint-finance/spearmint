
# PersonCreate

Schema to create a person.

## Properties

Name | Type
------------ | -------------
`name` | string
`isActive` | boolean

## Example

```typescript
import type { PersonCreate } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "name": null,
  "isActive": null,
} satisfies PersonCreate

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as PersonCreate
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


