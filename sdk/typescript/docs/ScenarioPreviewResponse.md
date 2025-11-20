
# ScenarioPreviewResponse


## Properties

Name | Type
------------ | -------------
`baselineSeries` | [Array&lt;SeriesPoint&gt;](SeriesPoint.md)
`scenarioSeries` | [Array&lt;SeriesPoint&gt;](SeriesPoint.md)
`kpis` | [ScenarioKPIs](ScenarioKPIs.md)
`deltas` | { [key: string]: string; }
`generatedAt` | Date

## Example

```typescript
import type { ScenarioPreviewResponse } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "baselineSeries": null,
  "scenarioSeries": null,
  "kpis": null,
  "deltas": null,
  "generatedAt": null,
} satisfies ScenarioPreviewResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as ScenarioPreviewResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


