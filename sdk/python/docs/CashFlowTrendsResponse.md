# CashFlowTrendsResponse

Response for cash flow trends.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**trends** | [**List[CashFlowTrendPoint]**](CashFlowTrendPoint.md) | Cash flow trend data | 
**period_type** | [**TimePeriodEnum**](TimePeriodEnum.md) | Period granularity | 
**mode** | [**AnalysisModeEnumOutput**](AnalysisModeEnumOutput.md) | Analysis mode used | 

## Example

```python
from spearmint_sdk.models.cash_flow_trends_response import CashFlowTrendsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CashFlowTrendsResponse from a JSON string
cash_flow_trends_response_instance = CashFlowTrendsResponse.from_json(json)
# print the JSON string representation of the object
print(CashFlowTrendsResponse.to_json())

# convert the object into a dict
cash_flow_trends_response_dict = cash_flow_trends_response_instance.to_dict()
# create an instance of CashFlowTrendsResponse from a dict
cash_flow_trends_response_from_dict = CashFlowTrendsResponse.from_dict(cash_flow_trends_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


