# ImportHistoryResponse

Schema for import history list response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**imports** | [**List[ImportHistoryItem]**](ImportHistoryItem.md) | List of imports | 
**total** | **int** | Total number of imports | 

## Example

```python
from spearmint_sdk.models.import_history_response import ImportHistoryResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ImportHistoryResponse from a JSON string
import_history_response_instance = ImportHistoryResponse.from_json(json)
# print the JSON string representation of the object
print(ImportHistoryResponse.to_json())

# convert the object into a dict
import_history_response_dict = import_history_response_instance.to_dict()
# create an instance of ImportHistoryResponse from a dict
import_history_response_from_dict = ImportHistoryResponse.from_dict(import_history_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


