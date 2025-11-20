# CashflowProjectionResponse

Response for cash flow projections.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**projection_type** | **str** | Type of projection | 
**historical_period** | [**HistoricalPeriod**](HistoricalPeriod.md) | Historical period details | 
**projection_period** | [**ProjectionPeriod**](ProjectionPeriod.md) | Projection period details | 
**method** | **str** | Projection method used | 
**confidence_level** | **float** | Confidence level | 
**projected_income** | **float** | Total projected income | 
**projected_expenses** | **float** | Total projected expenses | 
**projected_cashflow** | **float** | Total projected cash flow | 
**confidence_interval** | [**ConfidenceInterval**](ConfidenceInterval.md) | Cash flow confidence interval | 
**daily_projections** | [**List[CashflowDailyProjection]**](CashflowDailyProjection.md) | Daily cash flow projections | 
**scenarios** | [**Scenarios**](Scenarios.md) |  | [optional] 

## Example

```python
from spearmint_sdk.models.cashflow_projection_response import CashflowProjectionResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CashflowProjectionResponse from a JSON string
cashflow_projection_response_instance = CashflowProjectionResponse.from_json(json)
# print the JSON string representation of the object
print(CashflowProjectionResponse.to_json())

# convert the object into a dict
cashflow_projection_response_dict = cashflow_projection_response_instance.to_dict()
# create an instance of CashflowProjectionResponse from a dict
cashflow_projection_response_from_dict = CashflowProjectionResponse.from_dict(cashflow_projection_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


