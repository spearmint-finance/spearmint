# ReconciliationReportResponse

Response for reconciliation report.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**report_type** | **str** | Type of report | 
**period** | [**ReportPeriod**](ReportPeriod.md) | Report period | 
**mode** | **str** | Analysis mode (always &#39;complete&#39; for reconciliation) | 
**summary** | [**ReconciliationSummary**](ReconciliationSummary.md) | Summary statistics | 
**transactions** | [**List[TransactionDetail]**](TransactionDetail.md) | All transactions in period | 

## Example

```python
from spearmint_sdk.models.reconciliation_report_response import ReconciliationReportResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ReconciliationReportResponse from a JSON string
reconciliation_report_response_instance = ReconciliationReportResponse.from_json(json)
# print the JSON string representation of the object
print(ReconciliationReportResponse.to_json())

# convert the object into a dict
reconciliation_report_response_dict = reconciliation_report_response_instance.to_dict()
# create an instance of ReconciliationReportResponse from a dict
reconciliation_report_response_from_dict = ReconciliationReportResponse.from_dict(reconciliation_report_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


