# ScenarioRange

Range across scenarios.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cashflow_range** | **float** | Range of cash flow across scenarios | 
**income_range** | **float** | Range of income across scenarios | 
**expense_range** | **float** | Range of expenses across scenarios | 

## Example

```python
from spearmint_sdk.models.scenario_range import ScenarioRange

# TODO update the JSON string below
json = "{}"
# create an instance of ScenarioRange from a JSON string
scenario_range_instance = ScenarioRange.from_json(json)
# print the JSON string representation of the object
print(ScenarioRange.to_json())

# convert the object into a dict
scenario_range_dict = scenario_range_instance.to_dict()
# create an instance of ScenarioRange from a dict
scenario_range_from_dict = ScenarioRange.from_dict(scenario_range_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


