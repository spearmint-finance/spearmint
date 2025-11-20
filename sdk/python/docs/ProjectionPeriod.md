# ProjectionPeriod

Projection period information.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**start_date** | **str** | Start date of projection period | 
**end_date** | **str** | End date of projection period | 
**days** | **int** | Number of days in projection period | 

## Example

```python
from spearmint_sdk.models.projection_period import ProjectionPeriod

# TODO update the JSON string below
json = "{}"
# create an instance of ProjectionPeriod from a JSON string
projection_period_instance = ProjectionPeriod.from_json(json)
# print the JSON string representation of the object
print(ProjectionPeriod.to_json())

# convert the object into a dict
projection_period_dict = projection_period_instance.to_dict()
# create an instance of ProjectionPeriod from a dict
projection_period_from_dict = ProjectionPeriod.from_dict(projection_period_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


