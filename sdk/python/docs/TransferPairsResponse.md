# TransferPairsResponse

Response with detected transfer pairs.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**count** | **int** | Total number of pairs detected | 
**high_confidence** | **int** | Number of high-confidence pairs (&gt;&#x3D;0.8) | 
**pairs** | [**List[TransferPairDetection]**](TransferPairDetection.md) | List of detected pairs | 

## Example

```python
from spearmint_sdk.models.transfer_pairs_response import TransferPairsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of TransferPairsResponse from a JSON string
transfer_pairs_response_instance = TransferPairsResponse.from_json(json)
# print the JSON string representation of the object
print(TransferPairsResponse.to_json())

# convert the object into a dict
transfer_pairs_response_dict = transfer_pairs_response_instance.to_dict()
# create an instance of TransferPairsResponse from a dict
transfer_pairs_response_from_dict = TransferPairsResponse.from_dict(transfer_pairs_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


