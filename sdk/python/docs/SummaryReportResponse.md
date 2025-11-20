# SummaryReportResponse

Response for summary report.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**report_type** | **str** | Type of report | 
**period** | [**ReportPeriod**](ReportPeriod.md) | Report period | 
**mode** | **str** | Analysis mode used | 
**income** | [**IncomeSummary**](IncomeSummary.md) | Income summary | 
**expenses** | [**ExpenseSummary**](ExpenseSummary.md) | Expense summary | 
**cashflow** | [**CashflowSummary**](CashflowSummary.md) | Cash flow summary | 
**health_indicators** | [**HealthIndicators**](HealthIndicators.md) | Financial health indicators | 

## Example

```python
from spearmint_sdk.models.summary_report_response import SummaryReportResponse

# TODO update the JSON string below
json = "{}"
# create an instance of SummaryReportResponse from a JSON string
summary_report_response_instance = SummaryReportResponse.from_json(json)
# print the JSON string representation of the object
print(SummaryReportResponse.to_json())

# convert the object into a dict
summary_report_response_dict = summary_report_response_instance.to_dict()
# create an instance of SummaryReportResponse from a dict
summary_report_response_from_dict = SummaryReportResponse.from_dict(summary_report_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


