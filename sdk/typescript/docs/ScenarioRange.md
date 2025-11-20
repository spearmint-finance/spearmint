
# ScenarioRange

Range across scenarios.

## Properties

Name | Type
------------ | -------------
`cashflowRange` | number
`incomeRange` | number
`expenseRange` | number

## Example

```typescript
import type { ScenarioRange } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "cashflowRange": null,
  "incomeRange": null,
  "expenseRange": null,
} satisfies ScenarioRange

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as ScenarioRange
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


