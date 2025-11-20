# ApplyRulesResponse

Schema for apply rules response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dry_run** | **bool** | Whether this was a dry run | 
**total_rules_processed** | **int** | Number of rules processed | 
**total_transactions_updated** | **int** | Total transactions updated/would be updated | 
**rules_applied** | **List[Dict[str, object]]** | Details of each rule application | 

## Example

```python
from spearmint_sdk.models.apply_rules_response import ApplyRulesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ApplyRulesResponse from a JSON string
apply_rules_response_instance = ApplyRulesResponse.from_json(json)
# print the JSON string representation of the object
print(ApplyRulesResponse.to_json())

# convert the object into a dict
apply_rules_response_dict = apply_rules_response_instance.to_dict()
# create an instance of ApplyRulesResponse from a dict
apply_rules_response_from_dict = ApplyRulesResponse.from_dict(apply_rules_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


