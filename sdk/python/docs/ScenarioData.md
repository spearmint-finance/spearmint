# ScenarioData

Scenario analysis data.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**income** | **float** | Projected income in scenario | 
**expenses** | **float** | Projected expenses in scenario | 
**cashflow** | **float** | Projected cash flow in scenario | 
**description** | **str** | Scenario description | 

## Example

```python
from spearmint_sdk.models.scenario_data import ScenarioData

# TODO update the JSON string below
json = "{}"
# create an instance of ScenarioData from a JSON string
scenario_data_instance = ScenarioData.from_json(json)
# print the JSON string representation of the object
print(ScenarioData.to_json())

# convert the object into a dict
scenario_data_dict = scenario_data_instance.to_dict()
# create an instance of ScenarioData from a dict
scenario_data_from_dict = ScenarioData.from_dict(scenario_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


