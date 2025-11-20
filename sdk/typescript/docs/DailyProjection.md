
# DailyProjection

Daily projection data point.

## Properties

Name | Type
------------ | -------------
`date` | string
`projectedValue` | number
`lowerBound` | number
`upperBound` | number

## Example

```typescript
import type { DailyProjection } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "date": null,
  "projectedValue": null,
  "lowerBound": null,
  "upperBound": null,
} satisfies DailyProjection

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as DailyProjection
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


