# ScenarioKPIs


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**runway_months** | **float** |  | 
**min_balance** | **str** |  | 
**coverage_by_person** | **Dict[str, float]** |  | [optional] 
**monthly_shortfall_by_person** | **Dict[str, str]** |  | [optional] 

## Example

```python
from spearmint_sdk.models.scenario_kpis import ScenarioKPIs

# TODO update the JSON string below
json = "{}"
# create an instance of ScenarioKPIs from a JSON string
scenario_kpis_instance = ScenarioKPIs.from_json(json)
# print the JSON string representation of the object
print(ScenarioKPIs.to_json())

# convert the object into a dict
scenario_kpis_dict = scenario_kpis_instance.to_dict()
# create an instance of ScenarioKPIs from a dict
scenario_kpis_from_dict = ScenarioKPIs.from_dict(scenario_kpis_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


