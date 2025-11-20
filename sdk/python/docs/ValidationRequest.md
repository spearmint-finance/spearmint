# ValidationRequest

Request for projection validation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**actual_values** | **List[float]** | Actual observed values | 
**predicted_values** | **List[float]** | Predicted values | 

## Example

```python
from spearmint_sdk.models.validation_request import ValidationRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ValidationRequest from a JSON string
validation_request_instance = ValidationRequest.from_json(json)
# print the JSON string representation of the object
print(ValidationRequest.to_json())

# convert the object into a dict
validation_request_dict = validation_request_instance.to_dict()
# create an instance of ValidationRequest from a dict
validation_request_from_dict = ValidationRequest.from_dict(validation_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


