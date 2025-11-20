# CashflowDailyProjection

Daily cash flow projection data point.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**var_date** | **str** | Projection date | 
**projected_income** | **float** | Projected income for the day | 
**projected_expenses** | **float** | Projected expenses for the day | 
**projected_cashflow** | **float** | Projected net cash flow | 
**cashflow_lower** | **float** | Lower confidence bound for cash flow | 
**cashflow_upper** | **float** | Upper confidence bound for cash flow | 

## Example

```python
from spearmint_sdk.models.cashflow_daily_projection import CashflowDailyProjection

# TODO update the JSON string below
json = "{}"
# create an instance of CashflowDailyProjection from a JSON string
cashflow_daily_projection_instance = CashflowDailyProjection.from_json(json)
# print the JSON string representation of the object
print(CashflowDailyProjection.to_json())

# convert the object into a dict
cashflow_daily_projection_dict = cashflow_daily_projection_instance.to_dict()
# create an instance of CashflowDailyProjection from a dict
cashflow_daily_projection_from_dict = CashflowDailyProjection.from_dict(cashflow_daily_projection_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


