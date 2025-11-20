# NetWorthResponse

Schema for net worth response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**assets** | **str** |  | 
**liabilities** | **str** |  | 
**net_worth** | **str** |  | 
**liquid_assets** | **str** |  | 
**investments** | **str** |  | 
**as_of_date** | **date** |  | 
**account_breakdown** | **Dict[str, object]** |  | [optional] 

## Example

```python
from spearmint_sdk.models.net_worth_response import NetWorthResponse

# TODO update the JSON string below
json = "{}"
# create an instance of NetWorthResponse from a JSON string
net_worth_response_instance = NetWorthResponse.from_json(json)
# print the JSON string representation of the object
print(NetWorthResponse.to_json())

# convert the object into a dict
net_worth_response_dict = net_worth_response_instance.to_dict()
# create an instance of NetWorthResponse from a dict
net_worth_response_from_dict = NetWorthResponse.from_dict(net_worth_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


