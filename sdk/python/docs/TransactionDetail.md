# TransactionDetail

Transaction detail for reconciliation report.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**var_date** | **str** | Transaction date | 
**description** | **str** | Transaction description | 
**category** | **str** | Category name | 
**type** | **str** | Transaction type (Income/Expense) | 
**amount** | **float** | Transaction amount | 
**classification** | **str** | Transaction classification | 
**source** | **str** | Data source | 

## Example

```python
from spearmint_sdk.models.transaction_detail import TransactionDetail

# TODO update the JSON string below
json = "{}"
# create an instance of TransactionDetail from a JSON string
transaction_detail_instance = TransactionDetail.from_json(json)
# print the JSON string representation of the object
print(TransactionDetail.to_json())

# convert the object into a dict
transaction_detail_dict = transaction_detail_instance.to_dict()
# create an instance of TransactionDetail from a dict
transaction_detail_from_dict = TransactionDetail.from_dict(transaction_detail_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


