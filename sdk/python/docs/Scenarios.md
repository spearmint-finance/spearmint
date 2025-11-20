# Scenarios

Scenario analysis results.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**expected** | [**ScenarioData**](ScenarioData.md) | Expected case scenario | 
**best_case** | [**ScenarioData**](ScenarioData.md) | Best case scenario | 
**worst_case** | [**ScenarioData**](ScenarioData.md) | Worst case scenario | 
**range** | [**ScenarioRange**](ScenarioRange.md) | Range across scenarios | 

## Example

```python
from spearmint_sdk.models.scenarios import Scenarios

# TODO update the JSON string below
json = "{}"
# create an instance of Scenarios from a JSON string
scenarios_instance = Scenarios.from_json(json)
# print the JSON string representation of the object
print(Scenarios.to_json())

# convert the object into a dict
scenarios_dict = scenarios_instance.to_dict()
# create an instance of Scenarios from a dict
scenarios_from_dict = Scenarios.from_dict(scenarios_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


