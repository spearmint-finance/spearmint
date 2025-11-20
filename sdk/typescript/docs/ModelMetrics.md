
# ModelMetrics

Model performance metrics.

## Properties

Name | Type
------------ | -------------
`rSquared` | number
`slope` | number
`intercept` | number
`stdError` | number
`movingAverage` | number
`stdDeviation` | number
`windowSize` | number
`smoothedValue` | number
`alpha` | number
`weightedAverage` | number
`weightedStd` | number
`sampleSize` | number

## Example

```typescript
import type { ModelMetrics } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "rSquared": null,
  "slope": null,
  "intercept": null,
  "stdError": null,
  "movingAverage": null,
  "stdDeviation": null,
  "windowSize": null,
  "smoothedValue": null,
  "alpha": null,
  "weightedAverage": null,
  "weightedStd": null,
  "sampleSize": null,
} satisfies ModelMetrics

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as ModelMetrics
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


