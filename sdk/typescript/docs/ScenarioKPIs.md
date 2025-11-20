
# ScenarioKPIs


## Properties

Name | Type
------------ | -------------
`runwayMonths` | number
`minBalance` | string
`coverageByPerson` | { [key: string]: number; }
`monthlyShortfallByPerson` | { [key: string]: string; }

## Example

```typescript
import type { ScenarioKPIs } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "runwayMonths": null,
  "minBalance": null,
  "coverageByPerson": null,
  "monthlyShortfallByPerson": null,
} satisfies ScenarioKPIs

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as ScenarioKPIs
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


