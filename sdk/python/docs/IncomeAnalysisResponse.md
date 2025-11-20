# IncomeAnalysisResponse

Response for income analysis.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total_income** | **str** | Total income amount | 
**transaction_count** | **int** | Number of income transactions | 
**average_transaction** | **str** | Average transaction amount | 
**breakdown_by_category** | [**Dict[str, CategoryBreakdown]**](CategoryBreakdown.md) | Breakdown by category | 
**period_start** | **date** |  | [optional] 
**period_end** | **date** |  | [optional] 
**mode** | [**AnalysisModeEnumOutput**](AnalysisModeEnumOutput.md) | Analysis mode used | 

## Example

```python
from spearmint_sdk.models.income_analysis_response import IncomeAnalysisResponse

# TODO update the JSON string below
json = "{}"
# create an instance of IncomeAnalysisResponse from a JSON string
income_analysis_response_instance = IncomeAnalysisResponse.from_json(json)
# print the JSON string representation of the object
print(IncomeAnalysisResponse.to_json())

# convert the object into a dict
income_analysis_response_dict = income_analysis_response_instance.to_dict()
# create an instance of IncomeAnalysisResponse from a dict
income_analysis_response_from_dict = IncomeAnalysisResponse.from_dict(income_analysis_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


