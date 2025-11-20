# TestCategoryRuleResponse

Schema for test category rule response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total_matches** | **int** | Total number of matching transactions | 
**sample_transactions** | **List[Dict[str, object]]** | Sample matching transactions | 
**has_more** | **bool** | Whether there are more matches beyond the limit | 

## Example

```python
from spearmint_sdk.models.test_category_rule_response import TestCategoryRuleResponse

# TODO update the JSON string below
json = "{}"
# create an instance of TestCategoryRuleResponse from a JSON string
test_category_rule_response_instance = TestCategoryRuleResponse.from_json(json)
# print the JSON string representation of the object
print(TestCategoryRuleResponse.to_json())

# convert the object into a dict
test_category_rule_response_dict = test_category_rule_response_instance.to_dict()
# create an instance of TestCategoryRuleResponse from a dict
test_category_rule_response_from_dict = TestCategoryRuleResponse.from_dict(test_category_rule_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


