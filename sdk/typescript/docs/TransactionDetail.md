
# TransactionDetail

Transaction detail for reconciliation report.

## Properties

Name | Type
------------ | -------------
`date` | string
`description` | string
`category` | string
`type` | string
`amount` | number
`classification` | string
`source` | string

## Example

```typescript
import type { TransactionDetail } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "date": null,
  "description": null,
  "category": null,
  "type": null,
  "amount": null,
  "classification": null,
  "source": null,
} satisfies TransactionDetail

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as TransactionDetail
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


