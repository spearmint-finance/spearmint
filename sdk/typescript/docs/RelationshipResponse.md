
# RelationshipResponse

Response model for a transaction relationship.

## Properties

Name | Type
------------ | -------------
`relationshipId` | number
`transactionId1` | number
`transactionId2` | number
`relationshipType` | string
`description` | string
`createdAt` | string

## Example

```typescript
import type { RelationshipResponse } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "relationshipId": null,
  "transactionId1": null,
  "transactionId2": null,
  "relationshipType": null,
  "description": null,
  "createdAt": null,
} satisfies RelationshipResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as RelationshipResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


