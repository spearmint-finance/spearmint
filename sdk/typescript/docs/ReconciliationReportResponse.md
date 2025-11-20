
# ReconciliationReportResponse

Response for reconciliation report.

## Properties

Name | Type
------------ | -------------
`reportType` | string
`period` | [ReportPeriod](ReportPeriod.md)
`mode` | string
`summary` | [ReconciliationSummary](ReconciliationSummary.md)
`transactions` | [Array&lt;TransactionDetail&gt;](TransactionDetail.md)

## Example

```typescript
import type { ReconciliationReportResponse } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "reportType": null,
  "period": null,
  "mode": null,
  "summary": null,
  "transactions": null,
} satisfies ReconciliationReportResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as ReconciliationReportResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


