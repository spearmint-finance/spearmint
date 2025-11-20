
# FinancialSummaryResponse

Response for comprehensive financial summary.

## Properties

Name | Type
------------ | -------------
`totalIncome` | string
`totalExpenses` | string
`netCashFlow` | string
`incomeCount` | number
`expenseCount` | number
`topIncomeCategories` | [Array&lt;TopCategory&gt;](TopCategory.md)
`topExpenseCategories` | [Array&lt;TopCategory&gt;](TopCategory.md)
`recentTransactions` | [Array&lt;RecentTransaction&gt;](RecentTransaction.md)
`financialHealth` | [FinancialHealthResponse](FinancialHealthResponse.md)
`periodStart` | Date
`periodEnd` | Date
`mode` | [AnalysisModeEnumOutput](AnalysisModeEnumOutput.md)

## Example

```typescript
import type { FinancialSummaryResponse } from '@spearmint-money/sdk'

// TODO: Update the object below with actual values
const example = {
  "totalIncome": null,
  "totalExpenses": null,
  "netCashFlow": null,
  "incomeCount": null,
  "expenseCount": null,
  "topIncomeCategories": null,
  "topExpenseCategories": null,
  "recentTransactions": null,
  "financialHealth": null,
  "periodStart": null,
  "periodEnd": null,
  "mode": null,
} satisfies FinancialSummaryResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as FinancialSummaryResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


