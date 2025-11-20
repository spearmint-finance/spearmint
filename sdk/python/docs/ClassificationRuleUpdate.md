# ClassificationRuleUpdate

Schema for updating a classification rule.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**rule_name** | **str** |  | [optional] 
**rule_priority** | **int** |  | [optional] 
**classification_id** | **int** |  | [optional] 
**is_active** | **bool** |  | [optional] 
**description_pattern** | **str** |  | [optional] 
**category_pattern** | **str** |  | [optional] 
**source_pattern** | **str** |  | [optional] 
**amount_min** | **float** |  | [optional] 
**amount_max** | **float** |  | [optional] 
**payment_method_pattern** | **str** |  | [optional] 

## Example

```python
from spearmint_sdk.models.classification_rule_update import ClassificationRuleUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of ClassificationRuleUpdate from a JSON string
classification_rule_update_instance = ClassificationRuleUpdate.from_json(json)
# print the JSON string representation of the object
print(ClassificationRuleUpdate.to_json())

# convert the object into a dict
classification_rule_update_dict = classification_rule_update_instance.to_dict()
# create an instance of ClassificationRuleUpdate from a dict
classification_rule_update_from_dict = ClassificationRuleUpdate.from_dict(classification_rule_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


