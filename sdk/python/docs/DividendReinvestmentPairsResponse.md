# DividendReinvestmentPairsResponse

Response with detected dividend reinvestment pairs.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**count** | **int** | Total number of pairs detected | 
**high_confidence** | **int** | Number of high-confidence pairs (&gt;&#x3D;0.8) | 
**pairs** | [**List[DividendReinvestmentPairDetection]**](DividendReinvestmentPairDetection.md) | List of detected pairs | 

## Example

```python
from spearmint_sdk.models.dividend_reinvestment_pairs_response import DividendReinvestmentPairsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of DividendReinvestmentPairsResponse from a JSON string
dividend_reinvestment_pairs_response_instance = DividendReinvestmentPairsResponse.from_json(json)
# print the JSON string representation of the object
print(DividendReinvestmentPairsResponse.to_json())

# convert the object into a dict
dividend_reinvestment_pairs_response_dict = dividend_reinvestment_pairs_response_instance.to_dict()
# create an instance of DividendReinvestmentPairsResponse from a dict
dividend_reinvestment_pairs_response_from_dict = DividendReinvestmentPairsResponse.from_dict(dividend_reinvestment_pairs_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


