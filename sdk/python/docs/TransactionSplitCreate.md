# TransactionSplitCreate

Create a split for a transaction.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**person_id** | **int** | Person ID for this split | 
**amount** | [**Amount1**](Amount1.md) |  | 

## Example

```python
from spearmint_sdk.models.transaction_split_create import TransactionSplitCreate

# TODO update the JSON string below
json = "{}"
# create an instance of TransactionSplitCreate from a JSON string
transaction_split_create_instance = TransactionSplitCreate.from_json(json)
# print the JSON string representation of the object
print(TransactionSplitCreate.to_json())

# convert the object into a dict
transaction_split_create_dict = transaction_split_create_instance.to_dict()
# create an instance of TransactionSplitCreate from a dict
transaction_split_create_from_dict = TransactionSplitCreate.from_dict(transaction_split_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


