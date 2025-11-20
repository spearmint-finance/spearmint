# DailyProjection

Daily projection data point.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**var_date** | **str** | Projection date | 
**projected_value** | **float** | Projected value for the day | 
**lower_bound** | **float** | Lower confidence bound | 
**upper_bound** | **float** | Upper confidence bound | 

## Example

```python
from spearmint_sdk.models.daily_projection import DailyProjection

# TODO update the JSON string below
json = "{}"
# create an instance of DailyProjection from a JSON string
daily_projection_instance = DailyProjection.from_json(json)
# print the JSON string representation of the object
print(DailyProjection.to_json())

# convert the object into a dict
daily_projection_dict = daily_projection_instance.to_dict()
# create an instance of DailyProjection from a dict
daily_projection_from_dict = DailyProjection.from_dict(daily_projection_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


