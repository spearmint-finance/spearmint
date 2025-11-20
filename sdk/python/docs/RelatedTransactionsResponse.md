# RelatedTransactionsResponse

Response with related transactions.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transaction_id** | **int** | Original transaction ID | 
**related_transactions** | [**List[RelatedTransactionInfo]**](RelatedTransactionInfo.md) | List of related transactions | 
**count** | **int** | Number of related transactions | 

## Example

```python
from spearmint_sdk.models.related_transactions_response import RelatedTransactionsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RelatedTransactionsResponse from a JSON string
related_transactions_response_instance = RelatedTransactionsResponse.from_json(json)
# print the JSON string representation of the object
print(RelatedTransactionsResponse.to_json())

# convert the object into a dict
related_transactions_response_dict = related_transactions_response_instance.to_dict()
# create an instance of RelatedTransactionsResponse from a dict
related_transactions_response_from_dict = RelatedTransactionsResponse.from_dict(related_transactions_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


