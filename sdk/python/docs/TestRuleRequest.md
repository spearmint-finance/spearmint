# TestRuleRequest

Schema for testing a classification rule.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**description_pattern** | **str** |  | [optional] 
**category_pattern** | **str** |  | [optional] 
**source_pattern** | **str** |  | [optional] 
**amount_min** | **float** |  | [optional] 
**amount_max** | **float** |  | [optional] 
**payment_method_pattern** | **str** |  | [optional] 

## Example

```python
from spearmint_sdk.models.test_rule_request import TestRuleRequest

# TODO update the JSON string below
json = "{}"
# create an instance of TestRuleRequest from a JSON string
test_rule_request_instance = TestRuleRequest.from_json(json)
# print the JSON string representation of the object
print(TestRuleRequest.to_json())

# convert the object into a dict
test_rule_request_dict = test_rule_request_instance.to_dict()
# create an instance of TestRuleRequest from a dict
test_rule_request_from_dict = TestRuleRequest.from_dict(test_rule_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


