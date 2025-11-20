
# ScenarioData

Scenario analysis data.

## Properties

Name | Type
------------ | -------------
`income` | number
`expenses` | number
`cashflow` | number
`description` | string

## Example

```typescript
import type { ScenarioData } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "income": null,
  "expenses": null,
  "cashflow": null,
  "description": null,
} satisfies ScenarioData

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as ScenarioData
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


