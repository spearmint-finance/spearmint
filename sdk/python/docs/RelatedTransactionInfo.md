# RelatedTransactionInfo

Information about a related transaction.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transaction** | [**TransactionSummary**](TransactionSummary.md) | Related transaction | 
**relationship_type** | **str** | Type of relationship | 
**relationship_description** | **str** |  | [optional] 

## Example

```python
from spearmint_sdk.models.related_transaction_info import RelatedTransactionInfo

# TODO update the JSON string below
json = "{}"
# create an instance of RelatedTransactionInfo from a JSON string
related_transaction_info_instance = RelatedTransactionInfo.from_json(json)
# print the JSON string representation of the object
print(RelatedTransactionInfo.to_json())

# convert the object into a dict
related_transaction_info_dict = related_transaction_info_instance.to_dict()
# create an instance of RelatedTransactionInfo from a dict
related_transaction_info_from_dict = RelatedTransactionInfo.from_dict(related_transaction_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


