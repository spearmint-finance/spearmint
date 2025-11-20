# ReconciliationCreate

Schema for creating a reconciliation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**statement_date** | **date** |  | 
**statement_balance** | [**StatementBalance**](StatementBalance.md) |  | 
**statement_cash_balance** | [**StatementCashBalance**](StatementCashBalance.md) |  | [optional] 
**statement_investment_value** | [**StatementInvestmentValue**](StatementInvestmentValue.md) |  | [optional] 
**notes** | **str** |  | [optional] 

## Example

```python
from spearmint_sdk.models.reconciliation_create import ReconciliationCreate

# TODO update the JSON string below
json = "{}"
# create an instance of ReconciliationCreate from a JSON string
reconciliation_create_instance = ReconciliationCreate.from_json(json)
# print the JSON string representation of the object
print(ReconciliationCreate.to_json())

# convert the object into a dict
reconciliation_create_dict = reconciliation_create_instance.to_dict()
# create an instance of ReconciliationCreate from a dict
reconciliation_create_from_dict = ReconciliationCreate.from_dict(reconciliation_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


