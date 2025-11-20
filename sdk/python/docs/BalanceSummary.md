# BalanceSummary

High-level balance summary.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total_assets** | **float** |  | 
**total_liabilities** | **float** |  | 
**net_worth** | **float** |  | 

## Example

```python
from spearmint_sdk.models.balance_summary import BalanceSummary

# TODO update the JSON string below
json = "{}"
# create an instance of BalanceSummary from a JSON string
balance_summary_instance = BalanceSummary.from_json(json)
# print the JSON string representation of the object
print(BalanceSummary.to_json())

# convert the object into a dict
balance_summary_dict = balance_summary_instance.to_dict()
# create an instance of BalanceSummary from a dict
balance_summary_from_dict = BalanceSummary.from_dict(balance_summary_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


