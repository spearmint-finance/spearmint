# AccountBalanceDetail

Detail for a single account balance.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**account_name** | **str** |  | 
**account_type** | **str** |  | 
**balance** | **float** |  | 
**transaction_count** | **int** |  | 
**income_sum** | **float** |  | 
**expense_sum** | **float** |  | 

## Example

```python
from spearmint_sdk.models.account_balance_detail import AccountBalanceDetail

# TODO update the JSON string below
json = "{}"
# create an instance of AccountBalanceDetail from a JSON string
account_balance_detail_instance = AccountBalanceDetail.from_json(json)
# print the JSON string representation of the object
print(AccountBalanceDetail.to_json())

# convert the object into a dict
account_balance_detail_dict = account_balance_detail_instance.to_dict()
# create an instance of AccountBalanceDetail from a dict
account_balance_detail_from_dict = AccountBalanceDetail.from_dict(account_balance_detail_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


