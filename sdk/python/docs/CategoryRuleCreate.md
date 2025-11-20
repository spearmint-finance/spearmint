# CategoryRuleCreate

Schema for creating a category rule.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**rule_name** | **str** | Name of the rule | 
**rule_priority** | **int** | Rule priority (lower &#x3D; higher priority) | [optional] [default to 100]
**category_id** | **int** | Category to assign when rule matches | 
**is_active** | **bool** | Whether the rule is active | [optional] [default to True]
**description_pattern** | **str** |  | [optional] 
**source_pattern** | **str** |  | [optional] 
**amount_min** | **float** |  | [optional] 
**amount_max** | **float** |  | [optional] 
**payment_method_pattern** | **str** |  | [optional] 
**transaction_type_pattern** | **str** |  | [optional] 

## Example

```python
from spearmint_sdk.models.category_rule_create import CategoryRuleCreate

# TODO update the JSON string below
json = "{}"
# create an instance of CategoryRuleCreate from a JSON string
category_rule_create_instance = CategoryRuleCreate.from_json(json)
# print the JSON string representation of the object
print(CategoryRuleCreate.to_json())

# convert the object into a dict
category_rule_create_dict = category_rule_create_instance.to_dict()
# create an instance of CategoryRuleCreate from a dict
category_rule_create_from_dict = CategoryRuleCreate.from_dict(category_rule_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


