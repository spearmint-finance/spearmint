
# ScenarioAdjusterIn

Inline adjuster for preview/simulate.

## Properties

Name | Type
------------ | -------------
`type` | string
`targetPersonId` | number
`params` | { [key: string]: any; }
`startDate` | Date
`endDate` | Date

## Example

```typescript
import type { ScenarioAdjusterIn } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "type": null,
  "targetPersonId": null,
  "params": null,
  "startDate": null,
  "endDate": null,
} satisfies ScenarioAdjusterIn

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as ScenarioAdjusterIn
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


