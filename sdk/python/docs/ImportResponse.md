# ImportResponse

Schema for import response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total_rows** | **int** | Total rows processed | 
**successful_rows** | **int** | Successfully imported rows | 
**failed_rows** | **int** | Failed rows | 
**classified_rows** | **int** | Automatically classified rows | 
**skipped_duplicates** | **int** | Skipped duplicate rows | 
**success_rate** | **float** | Success rate percentage | 
**errors** | [**List[ImportErrorDetail]**](ImportErrorDetail.md) | List of errors | [optional] 
**warnings** | **List[str]** | List of warnings | [optional] 

## Example

```python
from spearmint_sdk.models.import_response import ImportResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ImportResponse from a JSON string
import_response_instance = ImportResponse.from_json(json)
# print the JSON string representation of the object
print(ImportResponse.to_json())

# convert the object into a dict
import_response_dict = import_response_instance.to_dict()
# create an instance of ImportResponse from a dict
import_response_from_dict = ImportResponse.from_dict(import_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


