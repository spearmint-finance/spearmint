# FixResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**task_name** | **str** |  | 
**status** | **str** |  | 
**details** | **Dict[str, object]** |  | 
**rows_affected** | **int** |  | 

## Example

```python
from spearmint_sdk.models.fix_result import FixResult

# TODO update the JSON string below
json = "{}"
# create an instance of FixResult from a JSON string
fix_result_instance = FixResult.from_json(json)
# print the JSON string representation of the object
print(FixResult.to_json())

# convert the object into a dict
fix_result_dict = fix_result_instance.to_dict()
# create an instance of FixResult from a dict
fix_result_from_dict = FixResult.from_dict(fix_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


