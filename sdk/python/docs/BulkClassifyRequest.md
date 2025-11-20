# BulkClassifyRequest

Schema for bulk classification.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transaction_ids** | **List[int]** | List of transaction IDs to classify | 
**classification_id** | **int** | Classification ID to apply | 

## Example

```python
from spearmint_sdk.models.bulk_classify_request import BulkClassifyRequest

# TODO update the JSON string below
json = "{}"
# create an instance of BulkClassifyRequest from a JSON string
bulk_classify_request_instance = BulkClassifyRequest.from_json(json)
# print the JSON string representation of the object
print(BulkClassifyRequest.to_json())

# convert the object into a dict
bulk_classify_request_dict = bulk_classify_request_instance.to_dict()
# create an instance of BulkClassifyRequest from a dict
bulk_classify_request_from_dict = BulkClassifyRequest.from_dict(bulk_classify_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


