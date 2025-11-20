# BalanceResponse

Schema for balance responses.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**balance_id** | **int** |  | 
**account_id** | **int** |  | 
**balance_date** | **date** |  | 
**total_balance** | **str** |  | 
**balance_type** | **str** |  | 
**cash_balance** | **str** |  | 
**investment_value** | **str** |  | 
**notes** | **str** |  | 
**created_at** | **datetime** |  | 
**updated_at** | **datetime** |  | 

## Example

```python
from spearmint_sdk.models.balance_response import BalanceResponse

# TODO update the JSON string below
json = "{}"
# create an instance of BalanceResponse from a JSON string
balance_response_instance = BalanceResponse.from_json(json)
# print the JSON string representation of the object
print(BalanceResponse.to_json())

# convert the object into a dict
balance_response_dict = balance_response_instance.to_dict()
# create an instance of BalanceResponse from a dict
balance_response_from_dict = BalanceResponse.from_dict(balance_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


