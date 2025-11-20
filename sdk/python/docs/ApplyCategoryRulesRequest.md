# ApplyCategoryRulesRequest

Schema for applying category rules.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transaction_ids** | **List[int]** |  | [optional] 
**rule_ids** | **List[int]** |  | [optional] 
**force_recategorize** | **bool** | If True, recategorize even if already categorized | [optional] [default to False]

## Example

```python
from spearmint_sdk.models.apply_category_rules_request import ApplyCategoryRulesRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ApplyCategoryRulesRequest from a JSON string
apply_category_rules_request_instance = ApplyCategoryRulesRequest.from_json(json)
# print the JSON string representation of the object
print(ApplyCategoryRulesRequest.to_json())

# convert the object into a dict
apply_category_rules_request_dict = apply_category_rules_request_instance.to_dict()
# create an instance of ApplyCategoryRulesRequest from a dict
apply_category_rules_request_from_dict = ApplyCategoryRulesRequest.from_dict(apply_category_rules_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


