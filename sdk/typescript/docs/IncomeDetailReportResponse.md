
# IncomeDetailReportResponse

Response for detailed income report.

## Properties

Name | Type
------------ | -------------
`reportType` | string
`period` | [ReportPeriod](ReportPeriod.md)
`mode` | string
`totalIncome` | number
`transactionCount` | number
`averageTransaction` | number
`categories` | [Array&lt;CategoryDetail&gt;](CategoryDetail.md)

## Example

```typescript
import type { IncomeDetailReportResponse } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "reportType": null,
  "period": null,
  "mode": null,
  "totalIncome": null,
  "transactionCount": null,
  "averageTransaction": null,
  "categories": null,
} satisfies IncomeDetailReportResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as IncomeDetailReportResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


