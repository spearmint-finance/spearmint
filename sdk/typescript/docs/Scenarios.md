
# Scenarios

Scenario analysis results.

## Properties

Name | Type
------------ | -------------
`expected` | [ScenarioData](ScenarioData.md)
`bestCase` | [ScenarioData](ScenarioData.md)
`worstCase` | [ScenarioData](ScenarioData.md)
`range` | [ScenarioRange](ScenarioRange.md)

## Example

```typescript
import type { Scenarios } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "expected": null,
  "bestCase": null,
  "worstCase": null,
  "range": null,
} satisfies Scenarios

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as Scenarios
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


