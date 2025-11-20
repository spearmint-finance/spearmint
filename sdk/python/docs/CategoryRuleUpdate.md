# CategoryRuleUpdate

Schema for updating a category rule.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**rule_name** | **str** |  | [optional] 
**rule_priority** | **int** |  | [optional] 
**category_id** | **int** |  | [optional] 
**is_active** | **bool** |  | [optional] 
**description_pattern** | **str** |  | [optional] 
**source_pattern** | **str** |  | [optional] 
**amount_min** | **float** |  | [optional] 
**amount_max** | **float** |  | [optional] 
**payment_method_pattern** | **str** |  | [optional] 
**transaction_type_pattern** | **str** |  | [optional] 

## Example

```python
from spearmint_sdk.models.category_rule_update import CategoryRuleUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of CategoryRuleUpdate from a JSON string
category_rule_update_instance = CategoryRuleUpdate.from_json(json)
# print the JSON string representation of the object
print(CategoryRuleUpdate.to_json())

# convert the object into a dict
category_rule_update_dict = category_rule_update_instance.to_dict()
# create an instance of CategoryRuleUpdate from a dict
category_rule_update_from_dict = CategoryRuleUpdate.from_dict(category_rule_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


