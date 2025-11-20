# TestRuleResponse

Schema for rule test response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**matching_transactions** | **int** | Number of transactions that would match | 
**sample_transaction_ids** | **List[int]** | Sample transaction IDs (max 10) | 

## Example

```python
from spearmint_sdk.models.test_rule_response import TestRuleResponse

# TODO update the JSON string below
json = "{}"
# create an instance of TestRuleResponse from a JSON string
test_rule_response_instance = TestRuleResponse.from_json(json)
# print the JSON string representation of the object
print(TestRuleResponse.to_json())

# convert the object into a dict
test_rule_response_dict = test_rule_response_instance.to_dict()
# create an instance of TestRuleResponse from a dict
test_rule_response_from_dict = TestRuleResponse.from_dict(test_rule_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


