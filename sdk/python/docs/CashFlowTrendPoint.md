# CashFlowTrendPoint

Cash flow trend data point.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**period** | **str** | Period identifier | 
**income** | **str** | Income for period | 
**expenses** | **str** | Expenses for period | 
**net_cash_flow** | **str** | Net cash flow for period | 
**income_count** | **int** | Number of income transactions | 
**expense_count** | **int** | Number of expense transactions | 

## Example

```python
from spearmint_sdk.models.cash_flow_trend_point import CashFlowTrendPoint

# TODO update the JSON string below
json = "{}"
# create an instance of CashFlowTrendPoint from a JSON string
cash_flow_trend_point_instance = CashFlowTrendPoint.from_json(json)
# print the JSON string representation of the object
print(CashFlowTrendPoint.to_json())

# convert the object into a dict
cash_flow_trend_point_dict = cash_flow_trend_point_instance.to_dict()
# create an instance of CashFlowTrendPoint from a dict
cash_flow_trend_point_from_dict = CashFlowTrendPoint.from_dict(cash_flow_trend_point_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


