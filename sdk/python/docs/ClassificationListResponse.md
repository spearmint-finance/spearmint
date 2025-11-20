# ClassificationListResponse

Schema for list of classifications.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**classifications** | [**List[ClassificationResponse]**](ClassificationResponse.md) | List of classifications | 
**total** | **int** | Total number of classifications | 

## Example

```python
from spearmint_sdk.models.classification_list_response import ClassificationListResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ClassificationListResponse from a JSON string
classification_list_response_instance = ClassificationListResponse.from_json(json)
# print the JSON string representation of the object
print(ClassificationListResponse.to_json())

# convert the object into a dict
classification_list_response_dict = classification_list_response_instance.to_dict()
# create an instance of ClassificationListResponse from a dict
classification_list_response_from_dict = ClassificationListResponse.from_dict(classification_list_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


