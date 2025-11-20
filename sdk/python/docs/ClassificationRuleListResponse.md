# ClassificationRuleListResponse

Schema for list of classification rules.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**rules** | [**List[ClassificationRuleResponse]**](ClassificationRuleResponse.md) | List of classification rules | 
**total** | **int** | Total number of rules | 

## Example

```python
from spearmint_sdk.models.classification_rule_list_response import ClassificationRuleListResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ClassificationRuleListResponse from a JSON string
classification_rule_list_response_instance = ClassificationRuleListResponse.from_json(json)
# print the JSON string representation of the object
print(ClassificationRuleListResponse.to_json())

# convert the object into a dict
classification_rule_list_response_dict = classification_rule_list_response_instance.to_dict()
# create an instance of ClassificationRuleListResponse from a dict
classification_rule_list_response_from_dict = ClassificationRuleListResponse.from_dict(classification_rule_list_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


