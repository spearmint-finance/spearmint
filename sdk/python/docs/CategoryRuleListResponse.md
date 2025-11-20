# CategoryRuleListResponse

Schema for category rule list response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**rules** | [**List[CategoryRuleResponse]**](CategoryRuleResponse.md) | List of category rules | 
**total** | **int** | Total number of rules | 

## Example

```python
from spearmint_sdk.models.category_rule_list_response import CategoryRuleListResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CategoryRuleListResponse from a JSON string
category_rule_list_response_instance = CategoryRuleListResponse.from_json(json)
# print the JSON string representation of the object
print(CategoryRuleListResponse.to_json())

# convert the object into a dict
category_rule_list_response_dict = category_rule_list_response_instance.to_dict()
# create an instance of CategoryRuleListResponse from a dict
category_rule_list_response_from_dict = CategoryRuleListResponse.from_dict(category_rule_list_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


