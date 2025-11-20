# RelationshipCreateRequest

Request to create a relationship between transactions.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transaction_id_1** | **int** | First transaction ID | 
**transaction_id_2** | **int** | Second transaction ID | 
**relationship_type** | **str** | Relationship type (TRANSFER_PAIR, CC_PAYMENT_RECEIPT, REIMBURSEMENT_PAIR, etc.) | 
**description** | **str** |  | [optional] 

## Example

```python
from spearmint_sdk.models.relationship_create_request import RelationshipCreateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RelationshipCreateRequest from a JSON string
relationship_create_request_instance = RelationshipCreateRequest.from_json(json)
# print the JSON string representation of the object
print(RelationshipCreateRequest.to_json())

# convert the object into a dict
relationship_create_request_dict = relationship_create_request_instance.to_dict()
# create an instance of RelationshipCreateRequest from a dict
relationship_create_request_from_dict = RelationshipCreateRequest.from_dict(relationship_create_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


