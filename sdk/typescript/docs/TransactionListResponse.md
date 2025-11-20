
# TransactionListResponse

Schema for transaction list response.

## Properties

Name | Type
------------ | -------------
`transactions` | [Array&lt;TransactionResponse&gt;](TransactionResponse.md)
`total` | number
`limit` | number
`offset` | number
`summary` | { [key: string]: any; }

## Example

```typescript
import type { TransactionListResponse } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "transactions": null,
  "total": null,
  "limit": null,
  "offset": null,
  "summary": null,
} satisfies TransactionListResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as TransactionListResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


