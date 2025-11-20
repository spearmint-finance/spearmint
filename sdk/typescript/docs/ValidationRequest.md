
# ValidationRequest

Request for projection validation.

## Properties

Name | Type
------------ | -------------
`actualValues` | Array&lt;number&gt;
`predictedValues` | Array&lt;number&gt;

## Example

```typescript
import type { ValidationRequest } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "actualValues": null,
  "predictedValues": null,
} satisfies ValidationRequest

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as ValidationRequest
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


