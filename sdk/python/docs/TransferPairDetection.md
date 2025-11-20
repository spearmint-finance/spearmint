# TransferPairDetection

Detected transfer pair.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transaction_1** | [**TransactionSummary**](TransactionSummary.md) | First transaction | 
**transaction_2** | [**TransactionSummary**](TransactionSummary.md) | Second transaction | 
**confidence** | **float** | Confidence score (0-1) | 
**amount_difference** | **str** | Difference in amounts | 
**date_difference_days** | **int** | Days between transactions | 
**relationship_type** | **str** | Suggested relationship type | 

## Example

```python
from spearmint_sdk.models.transfer_pair_detection import TransferPairDetection

# TODO update the JSON string below
json = "{}"
# create an instance of TransferPairDetection from a JSON string
transfer_pair_detection_instance = TransferPairDetection.from_json(json)
# print the JSON string representation of the object
print(TransferPairDetection.to_json())

# convert the object into a dict
transfer_pair_detection_dict = transfer_pair_detection_instance.to_dict()
# create an instance of TransferPairDetection from a dict
transfer_pair_detection_from_dict = TransferPairDetection.from_dict(transfer_pair_detection_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


