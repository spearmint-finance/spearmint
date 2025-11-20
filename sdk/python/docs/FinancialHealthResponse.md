# FinancialHealthResponse

Response for financial health indicators.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**income_to_expense_ratio** | **float** |  | [optional] 
**savings_rate** | **float** |  | [optional] 
**average_daily_income** | **str** | Average daily income | 
**average_daily_expense** | **str** | Average daily expense | 
**net_daily_cash_flow** | **str** | Net daily cash flow | 
**period_start** | **date** |  | [optional] 
**period_end** | **date** |  | [optional] 

## Example

```python
from spearmint_sdk.models.financial_health_response import FinancialHealthResponse

# TODO update the JSON string below
json = "{}"
# create an instance of FinancialHealthResponse from a JSON string
financial_health_response_instance = FinancialHealthResponse.from_json(json)
# print the JSON string representation of the object
print(FinancialHealthResponse.to_json())

# convert the object into a dict
financial_health_response_dict = financial_health_response_instance.to_dict()
# create an instance of FinancialHealthResponse from a dict
financial_health_response_from_dict = FinancialHealthResponse.from_dict(financial_health_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


