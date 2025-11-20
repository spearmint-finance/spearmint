# CreditCardPairsResponse

Response with detected credit card pairs.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**count** | **int** | Total number of pairs detected | 
**high_confidence** | **int** | Number of high-confidence pairs (&gt;&#x3D;0.8) | 
**pairs** | [**List[CreditCardPairDetection]**](CreditCardPairDetection.md) | List of detected pairs | 

## Example

```python
from spearmint_sdk.models.credit_card_pairs_response import CreditCardPairsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreditCardPairsResponse from a JSON string
credit_card_pairs_response_instance = CreditCardPairsResponse.from_json(json)
# print the JSON string representation of the object
print(CreditCardPairsResponse.to_json())

# convert the object into a dict
credit_card_pairs_response_dict = credit_card_pairs_response_instance.to_dict()
# create an instance of CreditCardPairsResponse from a dict
credit_card_pairs_response_from_dict = CreditCardPairsResponse.from_dict(credit_card_pairs_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


