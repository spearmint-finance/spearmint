# TransactionSplitRead

Read model for a transaction split.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**split_id** | **int** |  | 
**transaction_id** | **int** |  | 
**person_id** | **int** |  | 
**amount** | **str** |  | 
**created_at** | **datetime** |  | 

## Example

```python
from spearmint_sdk.models.transaction_split_read import TransactionSplitRead

# TODO update the JSON string below
json = "{}"
# create an instance of TransactionSplitRead from a JSON string
transaction_split_read_instance = TransactionSplitRead.from_json(json)
# print the JSON string representation of the object
print(TransactionSplitRead.to_json())

# convert the object into a dict
transaction_split_read_dict = transaction_split_read_instance.to_dict()
# create an instance of TransactionSplitRead from a dict
transaction_split_read_from_dict = TransactionSplitRead.from_dict(transaction_split_read_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


