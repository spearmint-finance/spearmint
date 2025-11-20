# HistoricalPeriod

Historical period information.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**start_date** | **str** | Start date of historical period | 
**end_date** | **str** | End date of historical period | 
**days** | **int** | Number of days in historical period | 
**total_income** | **float** |  | [optional] 
**total_expenses** | **float** |  | [optional] 
**average_daily** | **float** | Average daily value | 

## Example

```python
from spearmint_sdk.models.historical_period import HistoricalPeriod

# TODO update the JSON string below
json = "{}"
# create an instance of HistoricalPeriod from a JSON string
historical_period_instance = HistoricalPeriod.from_json(json)
# print the JSON string representation of the object
print(HistoricalPeriod.to_json())

# convert the object into a dict
historical_period_dict = historical_period_instance.to_dict()
# create an instance of HistoricalPeriod from a dict
historical_period_from_dict = HistoricalPeriod.from_dict(historical_period_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


