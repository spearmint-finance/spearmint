# ScenarioPreviewRequest

Scenario preview request body.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**horizon_months** | **int** |  | [optional] [default to 12]
**starting_balance** | [**StartingBalance**](StartingBalance.md) |  | [optional] 
**shared_expense_strategy** | **str** | Default split if no explicit splits present | [optional] [default to 'equal_split']
**adjusters** | [**List[ScenarioAdjusterIn]**](ScenarioAdjusterIn.md) |  | [optional] 

## Example

```python
from spearmint_sdk.models.scenario_preview_request import ScenarioPreviewRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ScenarioPreviewRequest from a JSON string
scenario_preview_request_instance = ScenarioPreviewRequest.from_json(json)
# print the JSON string representation of the object
print(ScenarioPreviewRequest.to_json())

# convert the object into a dict
scenario_preview_request_dict = scenario_preview_request_instance.to_dict()
# create an instance of ScenarioPreviewRequest from a dict
scenario_preview_request_from_dict = ScenarioPreviewRequest.from_dict(scenario_preview_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


