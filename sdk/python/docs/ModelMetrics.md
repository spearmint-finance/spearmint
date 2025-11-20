# ModelMetrics

Model performance metrics.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**r_squared** | **float** |  | [optional] 
**slope** | **float** |  | [optional] 
**intercept** | **float** |  | [optional] 
**std_error** | **float** |  | [optional] 
**moving_average** | **float** |  | [optional] 
**std_deviation** | **float** |  | [optional] 
**window_size** | **int** |  | [optional] 
**smoothed_value** | **float** |  | [optional] 
**alpha** | **float** |  | [optional] 
**weighted_average** | **float** |  | [optional] 
**weighted_std** | **float** |  | [optional] 
**sample_size** | **int** |  | [optional] 

## Example

```python
from spearmint_sdk.models.model_metrics import ModelMetrics

# TODO update the JSON string below
json = "{}"
# create an instance of ModelMetrics from a JSON string
model_metrics_instance = ModelMetrics.from_json(json)
# print the JSON string representation of the object
print(ModelMetrics.to_json())

# convert the object into a dict
model_metrics_dict = model_metrics_instance.to_dict()
# create an instance of ModelMetrics from a dict
model_metrics_from_dict = ModelMetrics.from_dict(model_metrics_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


