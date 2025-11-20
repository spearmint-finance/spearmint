# AutoClassifyRequest

Schema for auto-classification request.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transaction_ids** | **List[int]** |  | [optional] 
**force_reclassify** | **bool** | Force reclassification of already classified transactions | [optional] [default to False]

## Example

```python
from spearmint_sdk.models.auto_classify_request import AutoClassifyRequest

# TODO update the JSON string below
json = "{}"
# create an instance of AutoClassifyRequest from a JSON string
auto_classify_request_instance = AutoClassifyRequest.from_json(json)
# print the JSON string representation of the object
print(AutoClassifyRequest.to_json())

# convert the object into a dict
auto_classify_request_dict = auto_classify_request_instance.to_dict()
# create an instance of AutoClassifyRequest from a dict
auto_classify_request_from_dict = AutoClassifyRequest.from_dict(auto_classify_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


