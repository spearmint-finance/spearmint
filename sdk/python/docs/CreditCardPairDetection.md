# CreditCardPairDetection

Detected credit card payment/receipt pair.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payment** | [**TransactionSummary**](TransactionSummary.md) | Payment transaction | 
**receipt** | [**TransactionSummary**](TransactionSummary.md) | Receipt transaction | 
**confidence** | **float** | Confidence score (0-1) | 
**date_difference_days** | **int** | Days between transactions | 
**relationship_type** | **str** | Relationship type | 

## Example

```python
from spearmint_sdk.models.credit_card_pair_detection import CreditCardPairDetection

# TODO update the JSON string below
json = "{}"
# create an instance of CreditCardPairDetection from a JSON string
credit_card_pair_detection_instance = CreditCardPairDetection.from_json(json)
# print the JSON string representation of the object
print(CreditCardPairDetection.to_json())

# convert the object into a dict
credit_card_pair_detection_dict = credit_card_pair_detection_instance.to_dict()
# create an instance of CreditCardPairDetection from a dict
credit_card_pair_detection_from_dict = CreditCardPairDetection.from_dict(credit_card_pair_detection_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


