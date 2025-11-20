
# NetWorthResponse

Schema for net worth response.

## Properties

Name | Type
------------ | -------------
`assets` | string
`liabilities` | string
`netWorth` | string
`liquidAssets` | string
`investments` | string
`asOfDate` | Date
`accountBreakdown` | { [key: string]: any; }

## Example

```typescript
import type { NetWorthResponse } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "assets": null,
  "liabilities": null,
  "netWorth": null,
  "liquidAssets": null,
  "investments": null,
  "asOfDate": null,
  "accountBreakdown": null,
} satisfies NetWorthResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as NetWorthResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


