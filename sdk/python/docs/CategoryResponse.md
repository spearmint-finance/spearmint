# CategoryResponse

Schema for category response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**category_name** | **str** | Category name | 
**category_type** | **str** | Category type | 
**parent_category_id** | **int** |  | [optional] 
**description** | **str** |  | [optional] 
**is_transfer_category** | **bool** | Is transfer category | [optional] [default to False]
**category_id** | **int** | Category ID | 
**created_at** | **datetime** | Creation timestamp | 

## Example

```python
from spearmint_sdk.models.category_response import CategoryResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CategoryResponse from a JSON string
category_response_instance = CategoryResponse.from_json(json)
# print the JSON string representation of the object
print(CategoryResponse.to_json())

# convert the object into a dict
category_response_dict = category_response_instance.to_dict()
# create an instance of CategoryResponse from a dict
category_response_from_dict = CategoryResponse.from_dict(category_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


