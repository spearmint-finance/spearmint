# RecentTransaction

Recent transaction summary.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transaction_id** | **int** | Transaction ID | 
**transaction_date** | **date** | Transaction date | 
**amount** | **str** | Transaction amount | 
**transaction_type** | **str** | Transaction type (Income/Expense) | 
**category** | **str** | Category name | 
**description** | **str** |  | [optional] 

## Example

```python
from spearmint_sdk.models.recent_transaction import RecentTransaction

# TODO update the JSON string below
json = "{}"
# create an instance of RecentTransaction from a JSON string
recent_transaction_instance = RecentTransaction.from_json(json)
# print the JSON string representation of the object
print(RecentTransaction.to_json())

# convert the object into a dict
recent_transaction_dict = recent_transaction_instance.to_dict()
# create an instance of RecentTransaction from a dict
recent_transaction_from_dict = RecentTransaction.from_dict(recent_transaction_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


