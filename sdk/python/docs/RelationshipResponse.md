# RelationshipResponse

Response model for a transaction relationship.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**relationship_id** | **int** | Relationship ID | 
**transaction_id_1** | **int** | First transaction ID | 
**transaction_id_2** | **int** | Second transaction ID | 
**relationship_type** | **str** | Type of relationship | 
**description** | **str** |  | [optional] 
**created_at** | **str** | Creation timestamp | 

## Example

```python
from spearmint_sdk.models.relationship_response import RelationshipResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RelationshipResponse from a JSON string
relationship_response_instance = RelationshipResponse.from_json(json)
# print the JSON string representation of the object
print(RelationshipResponse.to_json())

# convert the object into a dict
relationship_response_dict = relationship_response_instance.to_dict()
# create an instance of RelationshipResponse from a dict
relationship_response_from_dict = RelationshipResponse.from_dict(relationship_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


