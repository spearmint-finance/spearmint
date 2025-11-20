# AccountCreate

Schema for creating a new account.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**account_name** | **str** |  | 
**account_type** | **str** |  | 
**account_subtype** | **str** |  | [optional] 
**institution_name** | **str** |  | [optional] 
**account_number_last4** | **str** |  | [optional] 
**currency** | **str** |  | [optional] [default to 'USD']
**notes** | **str** |  | [optional] 
**opening_balance** | [**OpeningBalance**](OpeningBalance.md) |  | [optional] 
**opening_balance_date** | **date** |  | [optional] 

## Example

```python
from spearmint_sdk.models.account_create import AccountCreate

# TODO update the JSON string below
json = "{}"
# create an instance of AccountCreate from a JSON string
account_create_instance = AccountCreate.from_json(json)
# print the JSON string representation of the object
print(AccountCreate.to_json())

# convert the object into a dict
account_create_dict = account_create_instance.to_dict()
# create an instance of AccountCreate from a dict
account_create_from_dict = AccountCreate.from_dict(account_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


