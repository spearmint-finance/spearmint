# ReimbursementPairDetection

Detected reimbursement pair.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**expense** | [**TransactionSummary**](TransactionSummary.md) | Original expense | 
**reimbursement** | [**TransactionSummary**](TransactionSummary.md) | Reimbursement income | 
**confidence** | **float** | Confidence score (0-1) | 
**date_difference_days** | **int** | Days between transactions | 
**relationship_type** | **str** | Relationship type | 

## Example

```python
from spearmint_sdk.models.reimbursement_pair_detection import ReimbursementPairDetection

# TODO update the JSON string below
json = "{}"
# create an instance of ReimbursementPairDetection from a JSON string
reimbursement_pair_detection_instance = ReimbursementPairDetection.from_json(json)
# print the JSON string representation of the object
print(ReimbursementPairDetection.to_json())

# convert the object into a dict
reimbursement_pair_detection_dict = reimbursement_pair_detection_instance.to_dict()
# create an instance of ReimbursementPairDetection from a dict
reimbursement_pair_detection_from_dict = ReimbursementPairDetection.from_dict(reimbursement_pair_detection_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


