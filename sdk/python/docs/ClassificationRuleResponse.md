# ClassificationRuleResponse

Schema for classification rule response.

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
**rule_id** | **int** | Rule ID | 
**created_at** | **datetime** | Creation timestamp | 
**updated_at** | **datetime** | Last update timestamp | 

## Example

```python
from spearmint_sdk.models.classification_rule_response import ClassificationRuleResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ClassificationRuleResponse from a JSON string
classification_rule_response_instance = ClassificationRuleResponse.from_json(json)
# print the JSON string representation of the object
print(ClassificationRuleResponse.to_json())

# convert the object into a dict
classification_rule_response_dict = classification_rule_response_instance.to_dict()
# create an instance of ClassificationRuleResponse from a dict
classification_rule_response_from_dict = ClassificationRuleResponse.from_dict(classification_rule_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


