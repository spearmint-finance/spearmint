# BalanceHistory

Schema for balance history response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**account_id** | **int** |  | 
**account_name** | **str** |  | 
**balances** | [**List[BalanceResponse]**](BalanceResponse.md) |  | 
**start_date** | **date** |  | 
**end_date** | **date** |  | 

## Example

```python
from spearmint_sdk.models.balance_history import BalanceHistory

# TODO update the JSON string below
json = "{}"
# create an instance of BalanceHistory from a JSON string
balance_history_instance = BalanceHistory.from_json(json)
# print the JSON string representation of the object
print(BalanceHistory.to_json())

# convert the object into a dict
balance_history_dict = balance_history_instance.to_dict()
# create an instance of BalanceHistory from a dict
balance_history_from_dict = BalanceHistory.from_dict(balance_history_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


