# ClassifyTransactionRequest

Schema for classifying a transaction.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**classification_id** | **int** | Classification ID to apply | 

## Example

```python
from spearmint_sdk.models.classify_transaction_request import ClassifyTransactionRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ClassifyTransactionRequest from a JSON string
classify_transaction_request_instance = ClassifyTransactionRequest.from_json(json)
# print the JSON string representation of the object
print(ClassifyTransactionRequest.to_json())

# convert the object into a dict
classify_transaction_request_dict = classify_transaction_request_instance.to_dict()
# create an instance of ClassifyTransactionRequest from a dict
classify_transaction_request_from_dict = ClassifyTransactionRequest.from_dict(classify_transaction_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


