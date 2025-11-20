# CalculatedBalance

Schema for calculated balance response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**account_id** | **int** |  | 
**as_of_date** | **date** |  | 
**total** | **str** |  | 
**cash** | **str** |  | [optional] 
**investments** | **str** |  | [optional] 
**based_on_transactions** | **int** |  | 

## Example

```python
from spearmint_sdk.models.calculated_balance import CalculatedBalance

# TODO update the JSON string below
json = "{}"
# create an instance of CalculatedBalance from a JSON string
calculated_balance_instance = CalculatedBalance.from_json(json)
# print the JSON string representation of the object
print(CalculatedBalance.to_json())

# convert the object into a dict
calculated_balance_dict = calculated_balance_instance.to_dict()
# create an instance of CalculatedBalance from a dict
calculated_balance_from_dict = CalculatedBalance.from_dict(calculated_balance_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


