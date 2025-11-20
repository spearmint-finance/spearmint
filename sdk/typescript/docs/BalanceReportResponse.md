
# BalanceReportResponse

Response for balance report.

## Properties

Name | Type
------------ | -------------
`reportType` | string
`summary` | [BalanceSummary](BalanceSummary.md)
`accounts` | [Array&lt;AccountBalanceDetail&gt;](AccountBalanceDetail.md)
`potentialIssues` | Array&lt;string&gt;

## Example

```typescript
import type { BalanceReportResponse } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "reportType": null,
  "summary": null,
  "accounts": null,
  "potentialIssues": null,
} satisfies BalanceReportResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as BalanceReportResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


