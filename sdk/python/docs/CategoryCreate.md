# CategoryCreate

Schema for creating a category.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**category_name** | **str** | Category name | 
**category_type** | **str** | Category type | 
**parent_category_id** | **int** |  | [optional] 
**description** | **str** |  | [optional] 
**is_transfer_category** | **bool** | Is transfer category | [optional] [default to False]

## Example

```python
from spearmint_sdk.models.category_create import CategoryCreate

# TODO update the JSON string below
json = "{}"
# create an instance of CategoryCreate from a JSON string
category_create_instance = CategoryCreate.from_json(json)
# print the JSON string representation of the object
print(CategoryCreate.to_json())

# convert the object into a dict
category_create_dict = category_create_instance.to_dict()
# create an instance of CategoryCreate from a dict
category_create_from_dict = CategoryCreate.from_dict(category_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


