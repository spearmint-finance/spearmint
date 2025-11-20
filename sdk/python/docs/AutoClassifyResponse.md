# AutoClassifyResponse

Schema for auto-classification response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total_processed** | **int** | Total transactions processed | 
**classified_count** | **int** | Number of transactions classified | 
**skipped_count** | **int** | Number of transactions skipped | 

## Example

```python
from spearmint_sdk.models.auto_classify_response import AutoClassifyResponse

# TODO update the JSON string below
json = "{}"
# create an instance of AutoClassifyResponse from a JSON string
auto_classify_response_instance = AutoClassifyResponse.from_json(json)
# print the JSON string representation of the object
print(AutoClassifyResponse.to_json())

# convert the object into a dict
auto_classify_response_dict = auto_classify_response_instance.to_dict()
# create an instance of AutoClassifyResponse from a dict
auto_classify_response_from_dict = AutoClassifyResponse.from_dict(auto_classify_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


