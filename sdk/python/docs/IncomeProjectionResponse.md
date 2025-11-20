# IncomeProjectionResponse

Response for income projections.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**projection_type** | **str** | Type of projection | 
**historical_period** | [**HistoricalPeriod**](HistoricalPeriod.md) | Historical period details | 
**projection_period** | [**ProjectionPeriod**](ProjectionPeriod.md) | Projection period details | 
**method** | **str** | Projection method used | 
**confidence_level** | **float** | Confidence level | 
**projected_total** | **float** | Total projected income | 
**confidence_interval** | [**ConfidenceInterval**](ConfidenceInterval.md) | Confidence interval | 
**daily_projections** | [**List[DailyProjection]**](DailyProjection.md) | Daily projection values | 
**model_metrics** | [**ModelMetrics**](ModelMetrics.md) | Model performance metrics | 

## Example

```python
from spearmint_sdk.models.income_projection_response import IncomeProjectionResponse

# TODO update the JSON string below
json = "{}"
# create an instance of IncomeProjectionResponse from a JSON string
income_projection_response_instance = IncomeProjectionResponse.from_json(json)
# print the JSON string representation of the object
print(IncomeProjectionResponse.to_json())

# convert the object into a dict
income_projection_response_dict = income_projection_response_instance.to_dict()
# create an instance of IncomeProjectionResponse from a dict
income_projection_response_from_dict = IncomeProjectionResponse.from_dict(income_projection_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


