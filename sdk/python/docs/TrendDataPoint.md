# TrendDataPoint

Single data point in a trend.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**period** | **str** | Period identifier (e.g., &#39;2025-01&#39;, &#39;2025-W01&#39;) | 
**value** | **str** | Value for the period | 
**count** | **int** | Number of transactions in period | 

## Example

```python
from spearmint_sdk.models.trend_data_point import TrendDataPoint

# TODO update the JSON string below
json = "{}"
# create an instance of TrendDataPoint from a JSON string
trend_data_point_instance = TrendDataPoint.from_json(json)
# print the JSON string representation of the object
print(TrendDataPoint.to_json())

# convert the object into a dict
trend_data_point_dict = trend_data_point_instance.to_dict()
# create an instance of TrendDataPoint from a dict
trend_data_point_from_dict = TrendDataPoint.from_dict(trend_data_point_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


