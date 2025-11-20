
# CategoryCreate

Schema for creating a category.

## Properties

Name | Type
------------ | -------------
`categoryName` | string
`categoryType` | string
`parentCategoryId` | number
`description` | string
`isTransferCategory` | boolean

## Example

```typescript
import type { CategoryCreate } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "categoryName": null,
  "categoryType": null,
  "parentCategoryId": null,
  "description": null,
  "isTransferCategory": null,
} satisfies CategoryCreate

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as CategoryCreate
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


