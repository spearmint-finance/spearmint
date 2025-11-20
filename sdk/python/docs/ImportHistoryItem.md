# ImportHistoryItem

Schema for a single import history item.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**import_id** | **int** | Import ID | 
**import_date** | **datetime** | Import date | 
**file_name** | **str** | File name | 
**total_rows** | **int** | Total rows | 
**successful_rows** | **int** | Successful rows | 
**failed_rows** | **int** | Failed rows | 
**classified_rows** | **int** | Classified rows | 
**import_mode** | **str** | Import mode | 
**success_rate** | **float** | Success rate percentage | 

## Example

```python
from spearmint_sdk.models.import_history_item import ImportHistoryItem

# TODO update the JSON string below
json = "{}"
# create an instance of ImportHistoryItem from a JSON string
import_history_item_instance = ImportHistoryItem.from_json(json)
# print the JSON string representation of the object
print(ImportHistoryItem.to_json())

# convert the object into a dict
import_history_item_dict = import_history_item_instance.to_dict()
# create an instance of ImportHistoryItem from a dict
import_history_item_from_dict = ImportHistoryItem.from_dict(import_history_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


