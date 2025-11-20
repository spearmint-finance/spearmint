# AccountResponse

Schema for account responses.

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
**account_id** | **int** |  | 
**is_active** | **bool** |  | 
**has_cash_component** | **bool** |  | 
**has_investment_component** | **bool** |  | 
**opening_balance** | **str** |  | 
**opening_balance_date** | **date** |  | 
**created_at** | **datetime** |  | 
**updated_at** | **datetime** |  | 
**current_balance** | **str** |  | [optional] 
**current_balance_date** | **date** |  | [optional] 
**cash_balance** | **str** |  | [optional] 
**investment_value** | **str** |  | [optional] 

## Example

```python
from spearmint_sdk.models.account_response import AccountResponse

# TODO update the JSON string below
json = "{}"
# create an instance of AccountResponse from a JSON string
account_response_instance = AccountResponse.from_json(json)
# print the JSON string representation of the object
print(AccountResponse.to_json())

# convert the object into a dict
account_response_dict = account_response_instance.to_dict()
# create an instance of AccountResponse from a dict
account_response_from_dict = AccountResponse.from_dict(account_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


