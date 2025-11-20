# ReconciliationResponse

Schema for reconciliation responses.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**reconciliation_id** | **int** |  | 
**account_id** | **int** |  | 
**statement_date** | **date** |  | 
**statement_balance** | **str** |  | 
**calculated_balance** | **str** |  | 
**statement_cash_balance** | **str** |  | 
**calculated_cash_balance** | **str** |  | 
**statement_investment_value** | **str** |  | 
**calculated_investment_value** | **str** |  | 
**discrepancy_amount** | **str** |  | 
**is_reconciled** | **bool** |  | 
**reconciled_at** | **datetime** |  | 
**reconciled_by** | **str** |  | 
**transactions_cleared_count** | **int** |  | 
**transactions_pending_count** | **int** |  | 
**notes** | **str** |  | 
**created_at** | **datetime** |  | 
**updated_at** | **datetime** |  | 

## Example

```python
from spearmint_sdk.models.reconciliation_response import ReconciliationResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ReconciliationResponse from a JSON string
reconciliation_response_instance = ReconciliationResponse.from_json(json)
# print the JSON string representation of the object
print(ReconciliationResponse.to_json())

# convert the object into a dict
reconciliation_response_dict = reconciliation_response_instance.to_dict()
# create an instance of ReconciliationResponse from a dict
reconciliation_response_from_dict = ReconciliationResponse.from_dict(reconciliation_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


