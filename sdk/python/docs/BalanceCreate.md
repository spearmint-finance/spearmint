# BalanceCreate

Schema for creating a balance snapshot.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**balance_date** | **date** |  | 
**total_balance** | [**TotalBalance**](TotalBalance.md) |  | 
**balance_type** | **str** |  | [optional] [default to 'statement']
**cash_balance** | [**CashBalance**](CashBalance.md) |  | [optional] 
**investment_value** | [**InvestmentValue**](InvestmentValue.md) |  | [optional] 
**notes** | **str** |  | [optional] 

## Example

```python
from spearmint_sdk.models.balance_create import BalanceCreate

# TODO update the JSON string below
json = "{}"
# create an instance of BalanceCreate from a JSON string
balance_create_instance = BalanceCreate.from_json(json)
# print the JSON string representation of the object
print(BalanceCreate.to_json())

# convert the object into a dict
balance_create_dict = balance_create_instance.to_dict()
# create an instance of BalanceCreate from a dict
balance_create_from_dict = BalanceCreate.from_dict(balance_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


