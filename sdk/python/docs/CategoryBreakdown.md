# CategoryBreakdown

Category breakdown data.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total** | **str** | Total amount for category | 
**count** | **int** | Number of transactions | 
**average** | **str** | Average transaction amount | 
**percentage** | **float** | Percentage of total | 

## Example

```python
from spearmint_sdk.models.category_breakdown import CategoryBreakdown

# TODO update the JSON string below
json = "{}"
# create an instance of CategoryBreakdown from a JSON string
category_breakdown_instance = CategoryBreakdown.from_json(json)
# print the JSON string representation of the object
print(CategoryBreakdown.to_json())

# convert the object into a dict
category_breakdown_dict = category_breakdown_instance.to_dict()
# create an instance of CategoryBreakdown from a dict
category_breakdown_from_dict = CategoryBreakdown.from_dict(category_breakdown_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


