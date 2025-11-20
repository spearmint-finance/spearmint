# AccountSummary

Schema for account summary with balance.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**account_id** | **int** |  | 
**account_name** | **str** |  | 
**account_type** | **str** |  | 
**institution** | **str** |  | 
**current_balance** | **str** |  | 
**balance_date** | **date** |  | 
**has_cash** | **bool** |  | 
**has_investments** | **bool** |  | 
**cash_balance** | **str** |  | [optional] 
**investment_value** | **str** |  | [optional] 

## Example

```python
from spearmint_sdk.models.account_summary import AccountSummary

# TODO update the JSON string below
json = "{}"
# create an instance of AccountSummary from a JSON string
account_summary_instance = AccountSummary.from_json(json)
# print the JSON string representation of the object
print(AccountSummary.to_json())

# convert the object into a dict
account_summary_dict = account_summary_instance.to_dict()
# create an instance of AccountSummary from a dict
account_summary_from_dict = AccountSummary.from_dict(account_summary_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


