# BulkClassifyResponse

Schema for bulk classification response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**success_count** | **int** | Number of successfully classified transactions | 
**failed_count** | **int** | Number of failed classifications | 
**failed_ids** | **List[int]** | IDs of transactions that failed | [optional] 

## Example

```python
from spearmint_sdk.models.bulk_classify_response import BulkClassifyResponse

# TODO update the JSON string below
json = "{}"
# create an instance of BulkClassifyResponse from a JSON string
bulk_classify_response_instance = BulkClassifyResponse.from_json(json)
# print the JSON string representation of the object
print(BulkClassifyResponse.to_json())

# convert the object into a dict
bulk_classify_response_dict = bulk_classify_response_instance.to_dict()
# create an instance of BulkClassifyResponse from a dict
bulk_classify_response_from_dict = BulkClassifyResponse.from_dict(bulk_classify_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


