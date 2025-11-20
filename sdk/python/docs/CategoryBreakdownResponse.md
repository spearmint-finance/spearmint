# CategoryBreakdownResponse

Response for category breakdown analysis.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**income_categories** | [**List[CategoryBreakdownItem]**](CategoryBreakdownItem.md) | Income category breakdown | 
**expense_categories** | [**List[CategoryBreakdownItem]**](CategoryBreakdownItem.md) | Expense category breakdown | 
**total_income** | **str** | Total income | 
**total_expenses** | **str** | Total expenses | 
**period_start** | **date** |  | [optional] 
**period_end** | **date** |  | [optional] 
**mode** | [**AnalysisModeEnumOutput**](AnalysisModeEnumOutput.md) | Analysis mode used | 

## Example

```python
from spearmint_sdk.models.category_breakdown_response import CategoryBreakdownResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CategoryBreakdownResponse from a JSON string
category_breakdown_response_instance = CategoryBreakdownResponse.from_json(json)
# print the JSON string representation of the object
print(CategoryBreakdownResponse.to_json())

# convert the object into a dict
category_breakdown_response_dict = category_breakdown_response_instance.to_dict()
# create an instance of CategoryBreakdownResponse from a dict
category_breakdown_response_from_dict = CategoryBreakdownResponse.from_dict(category_breakdown_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


