
# CategoryBreakdownItem

Category breakdown item with details.

## Properties

Name | Type
------------ | -------------
`categoryId` | number
`categoryName` | string
`categoryType` | string
`totalAmount` | string
`transactionCount` | number
`averageAmount` | string
`percentageOfTotal` | number
`percentageOfAll` | number

## Example

```typescript
import type { CategoryBreakdownItem } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "categoryId": null,
  "categoryName": null,
  "categoryType": null,
  "totalAmount": null,
  "transactionCount": null,
  "averageAmount": null,
  "percentageOfTotal": null,
  "percentageOfAll": null,
} satisfies CategoryBreakdownItem

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as CategoryBreakdownItem
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


