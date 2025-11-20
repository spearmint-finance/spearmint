# CashFlowResponse

Response for cash flow analysis.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**net_cash_flow** | **str** | Net cash flow (income - expenses) | 
**total_income** | **str** | Total income | 
**total_expenses** | **str** | Total expenses | 
**income_count** | **int** | Number of income transactions | 
**expense_count** | **int** | Number of expense transactions | 
**period_start** | **date** |  | [optional] 
**period_end** | **date** |  | [optional] 
**mode** | [**AnalysisModeEnumOutput**](AnalysisModeEnumOutput.md) | Analysis mode used | 

## Example

```python
from spearmint_sdk.models.cash_flow_response import CashFlowResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CashFlowResponse from a JSON string
cash_flow_response_instance = CashFlowResponse.from_json(json)
# print the JSON string representation of the object
print(CashFlowResponse.to_json())

# convert the object into a dict
cash_flow_response_dict = cash_flow_response_instance.to_dict()
# create an instance of CashFlowResponse from a dict
cash_flow_response_from_dict = CashFlowResponse.from_dict(cash_flow_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


