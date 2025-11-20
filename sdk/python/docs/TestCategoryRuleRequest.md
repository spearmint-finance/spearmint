# TestCategoryRuleRequest

Schema for testing a category rule.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**description_pattern** | **str** |  | [optional] 
**source_pattern** | **str** |  | [optional] 
**amount_min** | **float** |  | [optional] 
**amount_max** | **float** |  | [optional] 
**payment_method_pattern** | **str** |  | [optional] 
**transaction_type_pattern** | **str** |  | [optional] 
**limit** | **int** | Maximum number of matching transactions to return | [optional] [default to 10]

## Example

```python
from spearmint_sdk.models.test_category_rule_request import TestCategoryRuleRequest

# TODO update the JSON string below
json = "{}"
# create an instance of TestCategoryRuleRequest from a JSON string
test_category_rule_request_instance = TestCategoryRuleRequest.from_json(json)
# print the JSON string representation of the object
print(TestCategoryRuleRequest.to_json())

# convert the object into a dict
test_category_rule_request_dict = test_category_rule_request_instance.to_dict()
# create an instance of TestCategoryRuleRequest from a dict
test_category_rule_request_from_dict = TestCategoryRuleRequest.from_dict(test_category_rule_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


