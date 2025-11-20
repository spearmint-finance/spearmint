# ImportStatusResponse

Schema for import status response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**import_id** | **int** | Import ID | 
**status** | **str** | Import status (pending, processing, completed, failed) | 
**progress** | **float** | Progress percentage (0-100) | 
**current_row** | **int** | Current row being processed | 
**total_rows** | **int** | Total rows to process | 
**successful_rows** | **int** | Successfully processed rows | 
**failed_rows** | **int** | Failed rows | 
**message** | **str** |  | [optional] 
**started_at** | **datetime** |  | [optional] 
**completed_at** | **datetime** |  | [optional] 

## Example

```python
from spearmint_sdk.models.import_status_response import ImportStatusResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ImportStatusResponse from a JSON string
import_status_response_instance = ImportStatusResponse.from_json(json)
# print the JSON string representation of the object
print(ImportStatusResponse.to_json())

# convert the object into a dict
import_status_response_dict = import_status_response_instance.to_dict()
# create an instance of ImportStatusResponse from a dict
import_status_response_from_dict = ImportStatusResponse.from_dict(import_status_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


