
# RelationshipCreateRequest

Request to create a relationship between transactions.

## Properties

Name | Type
------------ | -------------
`transactionId1` | number
`transactionId2` | number
`relationshipType` | string
`description` | string

## Example

```typescript
import type { RelationshipCreateRequest } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "transactionId1": null,
  "transactionId2": null,
  "relationshipType": null,
  "description": null,
} satisfies RelationshipCreateRequest

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as RelationshipCreateRequest
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


