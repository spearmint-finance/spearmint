# DetectAllRelationshipsResponse

Response with all detected relationships.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transfer_pairs** | [**TransferPairsResponse**](TransferPairsResponse.md) | Transfer pair detections | 
**credit_card_pairs** | [**CreditCardPairsResponse**](CreditCardPairsResponse.md) | Credit card pair detections | 
**reimbursement_pairs** | [**ReimbursementPairsResponse**](ReimbursementPairsResponse.md) | Reimbursement pair detections | 
**dividend_reinvestment_pairs** | [**DividendReinvestmentPairsResponse**](DividendReinvestmentPairsResponse.md) | Dividend reinvestment pair detections | 
**total_detected** | **int** | Total relationships detected across all types | 
**auto_linked** | **bool** | Whether relationships were automatically created | 

## Example

```python
from spearmint_sdk.models.detect_all_relationships_response import DetectAllRelationshipsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of DetectAllRelationshipsResponse from a JSON string
detect_all_relationships_response_instance = DetectAllRelationshipsResponse.from_json(json)
# print the JSON string representation of the object
print(DetectAllRelationshipsResponse.to_json())

# convert the object into a dict
detect_all_relationships_response_dict = detect_all_relationships_response_instance.to_dict()
# create an instance of DetectAllRelationshipsResponse from a dict
detect_all_relationships_response_from_dict = DetectAllRelationshipsResponse.from_dict(detect_all_relationships_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


