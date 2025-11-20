# ApplyCategoryRulesResponse

Schema for apply category rules response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total_processed** | **int** | Total number of transactions processed | 
**categorized_count** | **int** | Number of transactions categorized | 
**skipped_count** | **int** | Number of transactions skipped | 
**rules_applied** | **int** | Number of rules applied | 

## Example

```python
from spearmint_sdk.models.apply_category_rules_response import ApplyCategoryRulesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ApplyCategoryRulesResponse from a JSON string
apply_category_rules_response_instance = ApplyCategoryRulesResponse.from_json(json)
# print the JSON string representation of the object
print(ApplyCategoryRulesResponse.to_json())

# convert the object into a dict
apply_category_rules_response_dict = apply_category_rules_response_instance.to_dict()
# create an instance of ApplyCategoryRulesResponse from a dict
apply_category_rules_response_from_dict = ApplyCategoryRulesResponse.from_dict(apply_category_rules_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


