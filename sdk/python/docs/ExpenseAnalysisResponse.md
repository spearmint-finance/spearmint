# ExpenseAnalysisResponse

Response for expense analysis.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total_expenses** | **str** | Total expense amount | 
**transaction_count** | **int** | Number of expense transactions | 
**average_transaction** | **str** | Average transaction amount | 
**breakdown_by_category** | [**Dict[str, CategoryBreakdown]**](CategoryBreakdown.md) | Breakdown by category | 
**top_categories** | [**List[TopCategory]**](TopCategory.md) | Top spending categories | 
**period_start** | **date** |  | [optional] 
**period_end** | **date** |  | [optional] 
**mode** | [**AnalysisModeEnumOutput**](AnalysisModeEnumOutput.md) | Analysis mode used | 

## Example

```python
from spearmint_sdk.models.expense_analysis_response import ExpenseAnalysisResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ExpenseAnalysisResponse from a JSON string
expense_analysis_response_instance = ExpenseAnalysisResponse.from_json(json)
# print the JSON string representation of the object
print(ExpenseAnalysisResponse.to_json())

# convert the object into a dict
expense_analysis_response_dict = expense_analysis_response_instance.to_dict()
# create an instance of ExpenseAnalysisResponse from a dict
expense_analysis_response_from_dict = ExpenseAnalysisResponse.from_dict(expense_analysis_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


