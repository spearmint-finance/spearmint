
# TrendsResponse

Response for trend analysis.

## Properties

Name | Type
------------ | -------------
`trends` | [Array&lt;TrendDataPoint&gt;](TrendDataPoint.md)
`periodType` | [TimePeriodEnum](TimePeriodEnum.md)
`mode` | [AnalysisModeEnumOutput](AnalysisModeEnumOutput.md)

## Example

```typescript
import type { TrendsResponse } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "trends": null,
  "periodType": null,
  "mode": null,
} satisfies TrendsResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as TrendsResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


