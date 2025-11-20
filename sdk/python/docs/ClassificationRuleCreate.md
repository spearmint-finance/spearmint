# ClassificationRuleCreate

Schema for creating a classification rule.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**rule_name** | **str** | Name of the rule | 
**rule_priority** | **int** | Rule priority (lower &#x3D; higher priority) | [optional] [default to 100]
**classification_id** | **int** | Classification to apply | 
**is_active** | **bool** | Whether the rule is active | [optional] [default to True]
**description_pattern** | **str** |  | [optional] 
**category_pattern** | **str** |  | [optional] 
**source_pattern** | **str** |  | [optional] 
**amount_min** | **float** |  | [optional] 
**amount_max** | **float** |  | [optional] 
**payment_method_pattern** | **str** |  | [optional] 

## Example

```python
from spearmint_sdk.models.classification_rule_create import ClassificationRuleCreate

# TODO update the JSON string below
json = "{}"
# create an instance of ClassificationRuleCreate from a JSON string
classification_rule_create_instance = ClassificationRuleCreate.from_json(json)
# print the JSON string representation of the object
print(ClassificationRuleCreate.to_json())

# convert the object into a dict
classification_rule_create_dict = classification_rule_create_instance.to_dict()
# create an instance of ClassificationRuleCreate from a dict
classification_rule_create_from_dict = ClassificationRuleCreate.from_dict(classification_rule_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


