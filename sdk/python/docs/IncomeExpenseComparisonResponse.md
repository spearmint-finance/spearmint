# IncomeExpenseComparisonResponse

Response for income vs expense comparison.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**income_analysis** | [**IncomeAnalysisResponse**](IncomeAnalysisResponse.md) | Income analysis | 
**expense_analysis** | [**ExpenseAnalysisResponse**](ExpenseAnalysisResponse.md) | Expense analysis | 
**cash_flow** | [**CashFlowResponse**](CashFlowResponse.md) | Cash flow summary | 
**comparison_metrics** | **Dict[str, object]** | Comparison metrics | 

## Example

```python
from spearmint_sdk.models.income_expense_comparison_response import IncomeExpenseComparisonResponse

# TODO update the JSON string below
json = "{}"
# create an instance of IncomeExpenseComparisonResponse from a JSON string
income_expense_comparison_response_instance = IncomeExpenseComparisonResponse.from_json(json)
# print the JSON string representation of the object
print(IncomeExpenseComparisonResponse.to_json())

# convert the object into a dict
income_expense_comparison_response_dict = income_expense_comparison_response_instance.to_dict()
# create an instance of IncomeExpenseComparisonResponse from a dict
income_expense_comparison_response_from_dict = IncomeExpenseComparisonResponse.from_dict(income_expense_comparison_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


