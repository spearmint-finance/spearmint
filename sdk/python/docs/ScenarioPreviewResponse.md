# ScenarioPreviewResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**baseline_series** | [**List[SeriesPoint]**](SeriesPoint.md) |  | 
**scenario_series** | [**List[SeriesPoint]**](SeriesPoint.md) |  | 
**kpis** | [**ScenarioKPIs**](ScenarioKPIs.md) |  | 
**deltas** | **Dict[str, str]** |  | 
**generated_at** | **datetime** |  | 

## Example

```python
from spearmint_sdk.models.scenario_preview_response import ScenarioPreviewResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ScenarioPreviewResponse from a JSON string
scenario_preview_response_instance = ScenarioPreviewResponse.from_json(json)
# print the JSON string representation of the object
print(ScenarioPreviewResponse.to_json())

# convert the object into a dict
scenario_preview_response_dict = scenario_preview_response_instance.to_dict()
# create an instance of ScenarioPreviewResponse from a dict
scenario_preview_response_from_dict = ScenarioPreviewResponse.from_dict(scenario_preview_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


