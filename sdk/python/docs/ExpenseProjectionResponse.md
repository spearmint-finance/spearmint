# ExpenseProjectionResponse

Response for expense projections.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**projection_type** | **str** | Type of projection | 
**historical_period** | [**HistoricalPeriod**](HistoricalPeriod.md) | Historical period details | 
**projection_period** | [**ProjectionPeriod**](ProjectionPeriod.md) | Projection period details | 
**method** | **str** | Projection method used | 
**confidence_level** | **float** | Confidence level | 
**projected_total** | **float** | Total projected expenses | 
**confidence_interval** | [**ConfidenceInterval**](ConfidenceInterval.md) | Confidence interval | 
**daily_projections** | [**List[DailyProjection]**](DailyProjection.md) | Daily projection values | 
**model_metrics** | [**ModelMetrics**](ModelMetrics.md) | Model performance metrics | 

## Example

```python
from spearmint_sdk.models.expense_projection_response import ExpenseProjectionResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ExpenseProjectionResponse from a JSON string
expense_projection_response_instance = ExpenseProjectionResponse.from_json(json)
# print the JSON string representation of the object
print(ExpenseProjectionResponse.to_json())

# convert the object into a dict
expense_projection_response_dict = expense_projection_response_instance.to_dict()
# create an instance of ExpenseProjectionResponse from a dict
expense_projection_response_from_dict = ExpenseProjectionResponse.from_dict(expense_projection_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


