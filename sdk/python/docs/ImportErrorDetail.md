# ImportErrorDetail

Schema for import error detail.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**row** | **int** | Row number | 
**var_field** | **str** | Field name | 
**message** | **str** | Error message | 
**value** | [**AnyOf**](AnyOf.md) | Invalid value | [optional] 

## Example

```python
from spearmint_sdk.models.import_error_detail import ImportErrorDetail

# TODO update the JSON string below
json = "{}"
# create an instance of ImportErrorDetail from a JSON string
import_error_detail_instance = ImportErrorDetail.from_json(json)
# print the JSON string representation of the object
print(ImportErrorDetail.to_json())

# convert the object into a dict
import_error_detail_dict = import_error_detail_instance.to_dict()
# create an instance of ImportErrorDetail from a dict
import_error_detail_from_dict = ImportErrorDetail.from_dict(import_error_detail_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


