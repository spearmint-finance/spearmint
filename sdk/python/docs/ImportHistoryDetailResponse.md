# ImportHistoryDetailResponse

Schema for detailed import history response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**import_id** | **int** | Import ID | 
**import_date** | **datetime** | Import date | 
**file_name** | **str** | File name | 
**file_path** | **str** | File path | 
**total_rows** | **int** | Total rows | 
**successful_rows** | **int** | Successful rows | 
**failed_rows** | **int** | Failed rows | 
**classified_rows** | **int** | Classified rows | 
**import_mode** | **str** | Import mode | 
**error_log** | **str** |  | [optional] 
**success_rate** | **float** | Success rate percentage | 

## Example

```python
from spearmint_sdk.models.import_history_detail_response import ImportHistoryDetailResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ImportHistoryDetailResponse from a JSON string
import_history_detail_response_instance = ImportHistoryDetailResponse.from_json(json)
# print the JSON string representation of the object
print(ImportHistoryDetailResponse.to_json())

# convert the object into a dict
import_history_detail_response_dict = import_history_detail_response_instance.to_dict()
# create an instance of ImportHistoryDetailResponse from a dict
import_history_detail_response_from_dict = ImportHistoryDetailResponse.from_dict(import_history_detail_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


