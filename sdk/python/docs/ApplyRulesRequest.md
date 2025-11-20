# ApplyRulesRequest

Schema for applying classification rules.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dry_run** | **bool** | If true, only preview changes without applying them | [optional] [default to True]
**rule_ids** | **List[int]** |  | [optional] 

## Example

```python
from spearmint_sdk.models.apply_rules_request import ApplyRulesRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ApplyRulesRequest from a JSON string
apply_rules_request_instance = ApplyRulesRequest.from_json(json)
# print the JSON string representation of the object
print(ApplyRulesRequest.to_json())

# convert the object into a dict
apply_rules_request_dict = apply_rules_request_instance.to_dict()
# create an instance of ApplyRulesRequest from a dict
apply_rules_request_from_dict = ApplyRulesRequest.from_dict(apply_rules_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


