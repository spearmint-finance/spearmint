# HoldingResponse

Schema for holding responses.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**holding_id** | **int** |  | 
**account_id** | **int** |  | 
**symbol** | **str** |  | 
**description** | **str** |  | 
**quantity** | **str** |  | 
**cost_basis** | **str** |  | 
**current_value** | **str** |  | 
**as_of_date** | **date** |  | 
**asset_class** | **str** |  | 
**sector** | **str** |  | 
**created_at** | **datetime** |  | 
**updated_at** | **datetime** |  | 
**gain_loss** | **str** |  | [optional] 
**gain_loss_percent** | **float** |  | [optional] 

## Example

```python
from spearmint_sdk.models.holding_response import HoldingResponse

# TODO update the JSON string below
json = "{}"
# create an instance of HoldingResponse from a JSON string
holding_response_instance = HoldingResponse.from_json(json)
# print the JSON string representation of the object
print(HoldingResponse.to_json())

# convert the object into a dict
holding_response_dict = holding_response_instance.to_dict()
# create an instance of HoldingResponse from a dict
holding_response_from_dict = HoldingResponse.from_dict(holding_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


