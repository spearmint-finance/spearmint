
# AccuracyMetrics

Projection accuracy metrics.

## Properties

Name | Type
------------ | -------------
`mape` | number
`rmse` | number
`mae` | number
`rSquared` | number
`sampleSize` | number
`accuracyGrade` | string

## Example

```typescript
import type { AccuracyMetrics } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "mape": null,
  "rmse": null,
  "mae": null,
  "rSquared": null,
  "sampleSize": null,
  "accuracyGrade": null,
} satisfies AccuracyMetrics

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as AccuracyMetrics
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


