
# AutoClassifyRequest

Schema for auto-classification request.

## Properties

Name | Type
------------ | -------------
`transactionIds` | Array&lt;number&gt;
`forceReclassify` | boolean

## Example

```typescript
import type { AutoClassifyRequest } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "transactionIds": null,
  "forceReclassify": null,
} satisfies AutoClassifyRequest

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as AutoClassifyRequest
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


