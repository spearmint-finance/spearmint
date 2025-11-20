# TrendsResponse

Response for trend analysis.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**trends** | [**List[TrendDataPoint]**](TrendDataPoint.md) | Trend data points | 
**period_type** | [**TimePeriodEnum**](TimePeriodEnum.md) | Period granularity | 
**mode** | [**AnalysisModeEnumOutput**](AnalysisModeEnumOutput.md) | Analysis mode used | 

## Example

```python
from spearmint_sdk.models.trends_response import TrendsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of TrendsResponse from a JSON string
trends_response_instance = TrendsResponse.from_json(json)
# print the JSON string representation of the object
print(TrendsResponse.to_json())

# convert the object into a dict
trends_response_dict = trends_response_instance.to_dict()
# create an instance of TrendsResponse from a dict
trends_response_from_dict = TrendsResponse.from_dict(trends_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


