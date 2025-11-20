
# ScenarioPreviewRequest

Scenario preview request body.

## Properties

Name | Type
------------ | -------------
`name` | string
`description` | string
`horizonMonths` | number
`startingBalance` | [StartingBalance](StartingBalance.md)
`sharedExpenseStrategy` | string
`adjusters` | [Array&lt;ScenarioAdjusterIn&gt;](ScenarioAdjusterIn.md)

## Example

```typescript
import type { ScenarioPreviewRequest } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "name": null,
  "description": null,
  "horizonMonths": null,
  "startingBalance": null,
  "sharedExpenseStrategy": null,
  "adjusters": null,
} satisfies ScenarioPreviewRequest

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as ScenarioPreviewRequest
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


