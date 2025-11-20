# TransactionUpdate

Schema for updating a transaction.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transaction_date** | **date** |  | [optional] 
**amount** | [**Amount2**](Amount2.md) |  | [optional] 
**transaction_type** | **str** |  | [optional] 
**category_id** | **int** |  | [optional] 
**source** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**payment_method** | **str** |  | [optional] 
**classification_id** | **int** |  | [optional] 
**include_in_analysis** | **bool** |  | [optional] 
**is_transfer** | **bool** |  | [optional] 
**transfer_account_from** | **str** |  | [optional] 
**transfer_account_to** | **str** |  | [optional] 
**notes** | **str** |  | [optional] 
**tag_names** | **List[str]** |  | [optional] 
**reapply_rules** | **bool** |  | [optional] 

## Example

```python
from spearmint_sdk.models.transaction_update import TransactionUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of TransactionUpdate from a JSON string
transaction_update_instance = TransactionUpdate.from_json(json)
# print the JSON string representation of the object
print(TransactionUpdate.to_json())

# convert the object into a dict
transaction_update_dict = transaction_update_instance.to_dict()
# create an instance of TransactionUpdate from a dict
transaction_update_from_dict = TransactionUpdate.from_dict(transaction_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


