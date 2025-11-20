# ConfidenceInterval

Confidence interval for projections.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**lower** | **float** | Lower bound of confidence interval | 
**upper** | **float** | Upper bound of confidence interval | 
**range** | **float** | Range of confidence interval | 

## Example

```python
from spearmint_sdk.models.confidence_interval import ConfidenceInterval

# TODO update the JSON string below
json = "{}"
# create an instance of ConfidenceInterval from a JSON string
confidence_interval_instance = ConfidenceInterval.from_json(json)
# print the JSON string representation of the object
print(ConfidenceInterval.to_json())

# convert the object into a dict
confidence_interval_dict = confidence_interval_instance.to_dict()
# create an instance of ConfidenceInterval from a dict
confidence_interval_from_dict = ConfidenceInterval.from_dict(confidence_interval_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


