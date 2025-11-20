# DividendReinvestmentPairDetection

Detected dividend reinvestment pair.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dividend** | [**TransactionSummary**](TransactionSummary.md) | Dividend income transaction | 
**reinvestment** | [**TransactionSummary**](TransactionSummary.md) | Reinvestment expense transaction | 
**confidence** | **float** | Confidence score (0-1) | 
**amount_difference** | **str** | Difference in amounts | 
**date_difference_days** | **int** | Days between transactions | 
**relationship_type** | **str** | Relationship type | 

## Example

```python
from spearmint_sdk.models.dividend_reinvestment_pair_detection import DividendReinvestmentPairDetection

# TODO update the JSON string below
json = "{}"
# create an instance of DividendReinvestmentPairDetection from a JSON string
dividend_reinvestment_pair_detection_instance = DividendReinvestmentPairDetection.from_json(json)
# print the JSON string representation of the object
print(DividendReinvestmentPairDetection.to_json())

# convert the object into a dict
dividend_reinvestment_pair_detection_dict = dividend_reinvestment_pair_detection_instance.to_dict()
# create an instance of DividendReinvestmentPairDetection from a dict
dividend_reinvestment_pair_detection_from_dict = DividendReinvestmentPairDetection.from_dict(dividend_reinvestment_pair_detection_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


