# ClassificationInfo

Classification information for transaction response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**classification_id** | **int** |  | 
**classification_name** | **str** |  | 
**classification_code** | **str** |  | 

## Example

```python
from spearmint_sdk.models.classification_info import ClassificationInfo

# TODO update the JSON string below
json = "{}"
# create an instance of ClassificationInfo from a JSON string
classification_info_instance = ClassificationInfo.from_json(json)
# print the JSON string representation of the object
print(ClassificationInfo.to_json())

# convert the object into a dict
classification_info_dict = classification_info_instance.to_dict()
# create an instance of ClassificationInfo from a dict
classification_info_from_dict = ClassificationInfo.from_dict(classification_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


