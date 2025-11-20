# TransactionClearRequest

Schema for clearing transactions.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transaction_ids** | **List[int]** |  | 
**cleared_date** | **date** |  | [optional] 

## Example

```python
from spearmint_sdk.models.transaction_clear_request import TransactionClearRequest

# TODO update the JSON string below
json = "{}"
# create an instance of TransactionClearRequest from a JSON string
transaction_clear_request_instance = TransactionClearRequest.from_json(json)
# print the JSON string representation of the object
print(TransactionClearRequest.to_json())

# convert the object into a dict
transaction_clear_request_dict = transaction_clear_request_instance.to_dict()
# create an instance of TransactionClearRequest from a dict
transaction_clear_request_from_dict = TransactionClearRequest.from_dict(transaction_clear_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


