# ReportPeriod

Report period information.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**start_date** | **str** | Start date of the period | 
**end_date** | **str** | End date of the period | 
**days** | **int** | Number of days in the period | 

## Example

```python
from spearmint_sdk.models.report_period import ReportPeriod

# TODO update the JSON string below
json = "{}"
# create an instance of ReportPeriod from a JSON string
report_period_instance = ReportPeriod.from_json(json)
# print the JSON string representation of the object
print(ReportPeriod.to_json())

# convert the object into a dict
report_period_dict = report_period_instance.to_dict()
# create an instance of ReportPeriod from a dict
report_period_from_dict = ReportPeriod.from_dict(report_period_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


