# TransactionResponse

Schema for transaction response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transaction_date** | **date** | Transaction date | 
**amount** | **str** | Transaction amount (can be negative for expenses) | 
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
**transaction_id** | **int** | Transaction ID | 
**related_transaction_id** | **int** |  | [optional] 
**category** | [**CategoryInfo**](CategoryInfo.md) |  | [optional] 
**classification** | [**ClassificationInfo**](ClassificationInfo.md) |  | [optional] 
**tags** | [**List[TagInfo]**](TagInfo.md) | Associated tags | [optional] 
**created_at** | **datetime** | Creation timestamp | 
**updated_at** | **datetime** | Last update timestamp | 

## Example

```python
from spearmint_sdk.models.transaction_response import TransactionResponse

# TODO update the JSON string below
json = "{}"
# create an instance of TransactionResponse from a JSON string
transaction_response_instance = TransactionResponse.from_json(json)
# print the JSON string representation of the object
print(TransactionResponse.to_json())

# convert the object into a dict
transaction_response_dict = transaction_response_instance.to_dict()
# create an instance of TransactionResponse from a dict
transaction_response_from_dict = TransactionResponse.from_dict(transaction_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


