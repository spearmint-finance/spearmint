# TopCategory

Top category data.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**category** | **str** | Category name | 
**amount** | **str** | Total amount | 
**count** | **int** | Number of transactions | 
**percentage** | **float** | Percentage of total | 

## Example

```python
from spearmint_sdk.models.top_category import TopCategory

# TODO update the JSON string below
json = "{}"
# create an instance of TopCategory from a JSON string
top_category_instance = TopCategory.from_json(json)
# print the JSON string representation of the object
print(TopCategory.to_json())

# convert the object into a dict
top_category_dict = top_category_instance.to_dict()
# create an instance of TopCategory from a dict
top_category_from_dict = TopCategory.from_dict(top_category_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


