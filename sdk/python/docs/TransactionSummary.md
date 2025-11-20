# TransactionSummary

Summary of a transaction for relationship display.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transaction_id** | **int** | Transaction ID | 
**transaction_date** | **date** | Transaction date | 
**amount** | **str** | Transaction amount | 
**transaction_type** | **str** | Income or Expense | 
**description** | **str** |  | [optional] 
**source** | **str** |  | [optional] 
**category_name** | **str** |  | [optional] 
**classification_name** | **str** |  | [optional] 

## Example

```python
from spearmint_sdk.models.transaction_summary import TransactionSummary

# TODO update the JSON string below
json = "{}"
# create an instance of TransactionSummary from a JSON string
transaction_summary_instance = TransactionSummary.from_json(json)
# print the JSON string representation of the object
print(TransactionSummary.to_json())

# convert the object into a dict
transaction_summary_dict = transaction_summary_instance.to_dict()
# create an instance of TransactionSummary from a dict
transaction_summary_from_dict = TransactionSummary.from_dict(transaction_summary_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


