# TransactionCreate

Schema for creating a transaction.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transaction_date** | **date** | Transaction date | 
**amount** | [**Amount**](Amount.md) |  | 
**transaction_type** | **str** | Transaction type | 
**category_id** | **int** | Category ID | 
**source** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**payment_method** | **str** |  | [optional] 
**classification_id** | **int** |  | [optional] 
**include_in_analysis** | **bool** | Include in analysis | [optional] [default to True]
**is_transfer** | **bool** | Is transfer transaction | [optional] [default to False]
**transfer_account_from** | **str** |  | [optional] 
**transfer_account_to** | **str** |  | [optional] 
**notes** | **str** |  | [optional] 
**tag_names** | **List[str]** |  | [optional] 

## Example

```python
from spearmint_sdk.models.transaction_create import TransactionCreate

# TODO update the JSON string below
json = "{}"
# create an instance of TransactionCreate from a JSON string
transaction_create_instance = TransactionCreate.from_json(json)
# print the JSON string representation of the object
print(TransactionCreate.to_json())

# convert the object into a dict
transaction_create_dict = transaction_create_instance.to_dict()
# create an instance of TransactionCreate from a dict
transaction_create_from_dict = TransactionCreate.from_dict(transaction_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


