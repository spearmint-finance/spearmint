# ReimbursementPairsResponse

Response with detected reimbursement pairs.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**count** | **int** | Total number of pairs detected | 
**high_confidence** | **int** | Number of high-confidence pairs (&gt;&#x3D;0.8) | 
**pairs** | [**List[ReimbursementPairDetection]**](ReimbursementPairDetection.md) | List of detected pairs | 

## Example

```python
from spearmint_sdk.models.reimbursement_pairs_response import ReimbursementPairsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ReimbursementPairsResponse from a JSON string
reimbursement_pairs_response_instance = ReimbursementPairsResponse.from_json(json)
# print the JSON string representation of the object
print(ReimbursementPairsResponse.to_json())

# convert the object into a dict
reimbursement_pairs_response_dict = reimbursement_pairs_response_instance.to_dict()
# create an instance of ReimbursementPairsResponse from a dict
reimbursement_pairs_response_from_dict = ReimbursementPairsResponse.from_dict(reimbursement_pairs_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


