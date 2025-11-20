# HoldingCreate

Schema for creating/updating a holding.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**symbol** | **str** |  | 
**quantity** | [**Quantity**](Quantity.md) |  | 
**as_of_date** | **date** |  | 
**description** | **str** |  | [optional] 
**cost_basis** | [**CostBasis**](CostBasis.md) |  | [optional] 
**current_value** | [**CurrentValue**](CurrentValue.md) |  | [optional] 
**asset_class** | **str** |  | [optional] 
**sector** | **str** |  | [optional] 

## Example

```python
from spearmint_sdk.models.holding_create import HoldingCreate

# TODO update the JSON string below
json = "{}"
# create an instance of HoldingCreate from a JSON string
holding_create_instance = HoldingCreate.from_json(json)
# print the JSON string representation of the object
print(HoldingCreate.to_json())

# convert the object into a dict
holding_create_dict = holding_create_instance.to_dict()
# create an instance of HoldingCreate from a dict
holding_create_from_dict = HoldingCreate.from_dict(holding_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


