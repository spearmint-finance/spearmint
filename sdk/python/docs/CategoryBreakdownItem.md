# CategoryBreakdownItem

Category breakdown item with details.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**category_id** | **int** | Category ID | 
**category_name** | **str** | Category name | 
**category_type** | **str** | Category type (Income/Expense) | 
**total_amount** | **str** | Total amount for category | 
**transaction_count** | **int** | Number of transactions | 
**average_amount** | **str** | Average transaction amount | 
**percentage_of_total** | **float** | Percentage of total income/expenses | 
**percentage_of_all** | **float** | Percentage of all transactions | 

## Example

```python
from spearmint_sdk.models.category_breakdown_item import CategoryBreakdownItem

# TODO update the JSON string below
json = "{}"
# create an instance of CategoryBreakdownItem from a JSON string
category_breakdown_item_instance = CategoryBreakdownItem.from_json(json)
# print the JSON string representation of the object
print(CategoryBreakdownItem.to_json())

# convert the object into a dict
category_breakdown_item_dict = category_breakdown_item_instance.to_dict()
# create an instance of CategoryBreakdownItem from a dict
category_breakdown_item_from_dict = CategoryBreakdownItem.from_dict(category_breakdown_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


