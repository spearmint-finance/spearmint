# FinancialSummaryResponse

Response for comprehensive financial summary.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total_income** | **str** | Total income for period | 
**total_expenses** | **str** | Total expenses for period | 
**net_cash_flow** | **str** | Net cash flow (income - expenses) | 
**income_count** | **int** | Number of income transactions | 
**expense_count** | **int** | Number of expense transactions | 
**top_income_categories** | [**List[TopCategory]**](TopCategory.md) | Top income categories | 
**top_expense_categories** | [**List[TopCategory]**](TopCategory.md) | Top expense categories | 
**recent_transactions** | [**List[RecentTransaction]**](RecentTransaction.md) | Recent transactions | 
**financial_health** | [**FinancialHealthResponse**](FinancialHealthResponse.md) | Financial health indicators | 
**period_start** | **date** |  | [optional] 
**period_end** | **date** |  | [optional] 
**mode** | [**AnalysisModeEnumOutput**](AnalysisModeEnumOutput.md) | Analysis mode used | 

## Example

```python
from spearmint_sdk.models.financial_summary_response import FinancialSummaryResponse

# TODO update the JSON string below
json = "{}"
# create an instance of FinancialSummaryResponse from a JSON string
financial_summary_response_instance = FinancialSummaryResponse.from_json(json)
# print the JSON string representation of the object
print(FinancialSummaryResponse.to_json())

# convert the object into a dict
financial_summary_response_dict = financial_summary_response_instance.to_dict()
# create an instance of FinancialSummaryResponse from a dict
financial_summary_response_from_dict = FinancialSummaryResponse.from_dict(financial_summary_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


