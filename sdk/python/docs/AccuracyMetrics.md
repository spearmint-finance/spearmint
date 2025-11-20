# AccuracyMetrics

Projection accuracy metrics.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**mape** | **float** | Mean Absolute Percentage Error | 
**rmse** | **float** | Root Mean Squared Error | 
**mae** | **float** | Mean Absolute Error | 
**r_squared** | **float** | R-squared value | 
**sample_size** | **int** | Number of data points | 
**accuracy_grade** | **str** | Accuracy grade (Excellent/Good/Acceptable/Poor/Very Poor) | 

## Example

```python
from spearmint_sdk.models.accuracy_metrics import AccuracyMetrics

# TODO update the JSON string below
json = "{}"
# create an instance of AccuracyMetrics from a JSON string
accuracy_metrics_instance = AccuracyMetrics.from_json(json)
# print the JSON string representation of the object
print(AccuracyMetrics.to_json())

# convert the object into a dict
accuracy_metrics_dict = accuracy_metrics_instance.to_dict()
# create an instance of AccuracyMetrics from a dict
accuracy_metrics_from_dict = AccuracyMetrics.from_dict(accuracy_metrics_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


