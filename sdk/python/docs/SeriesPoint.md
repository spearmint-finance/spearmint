# SeriesPoint


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**var_date** | **date** |  | 
**income** | **str** |  | 
**expenses** | **str** |  | 
**net_cf** | **str** |  | 
**by_person** | **Dict[str, Dict[str, str]]** |  | [optional] 

## Example

```python
from spearmint_sdk.models.series_point import SeriesPoint

# TODO update the JSON string below
json = "{}"
# create an instance of SeriesPoint from a JSON string
series_point_instance = SeriesPoint.from_json(json)
# print the JSON string representation of the object
print(SeriesPoint.to_json())

# convert the object into a dict
series_point_dict = series_point_instance.to_dict()
# create an instance of SeriesPoint from a dict
series_point_from_dict = SeriesPoint.from_dict(series_point_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


