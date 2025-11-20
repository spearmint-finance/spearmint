# HealthIndicators

Financial health indicators.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**income_to_expense_ratio** | **float** |  | [optional] 
**savings_rate** | **float** |  | [optional] 
**average_daily_income** | **float** | Average daily income | 
**average_daily_expense** | **float** | Average daily expense | 
**average_daily_cashflow** | **float** | Average daily cash flow | 

## Example

```python
from spearmint_sdk.models.health_indicators import HealthIndicators

# TODO update the JSON string below
json = "{}"
# create an instance of HealthIndicators from a JSON string
health_indicators_instance = HealthIndicators.from_json(json)
# print the JSON string representation of the object
print(HealthIndicators.to_json())

# convert the object into a dict
health_indicators_dict = health_indicators_instance.to_dict()
# create an instance of HealthIndicators from a dict
health_indicators_from_dict = HealthIndicators.from_dict(health_indicators_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


