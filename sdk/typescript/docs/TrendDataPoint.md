
# TrendDataPoint

Single data point in a trend.

## Properties

Name | Type
------------ | -------------
`period` | string
`value` | string
`count` | number

## Example

```typescript
import type { TrendDataPoint } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "period": null,
  "value": null,
  "count": null,
} satisfies TrendDataPoint

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as TrendDataPoint
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


