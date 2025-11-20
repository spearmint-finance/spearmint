# ScenarioAdjusterIn

Inline adjuster for preview/simulate.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** | Adjuster type: job_loss | income_reduction | expense_change | one_time | 
**target_person_id** | **int** |  | [optional] 
**params** | **Dict[str, object]** |  | [optional] 
**start_date** | **date** |  | [optional] 
**end_date** | **date** |  | [optional] 

## Example

```python
from spearmint_sdk.models.scenario_adjuster_in import ScenarioAdjusterIn

# TODO update the JSON string below
json = "{}"
# create an instance of ScenarioAdjusterIn from a JSON string
scenario_adjuster_in_instance = ScenarioAdjusterIn.from_json(json)
# print the JSON string representation of the object
print(ScenarioAdjusterIn.to_json())

# convert the object into a dict
scenario_adjuster_in_dict = scenario_adjuster_in_instance.to_dict()
# create an instance of ScenarioAdjusterIn from a dict
scenario_adjuster_in_from_dict = ScenarioAdjusterIn.from_dict(scenario_adjuster_in_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


