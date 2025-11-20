# BalanceReportResponse

Response for balance report.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**report_type** | **str** | Type of report (balance) | 
**summary** | [**BalanceSummary**](BalanceSummary.md) |  | 
**accounts** | [**List[AccountBalanceDetail]**](AccountBalanceDetail.md) |  | 
**potential_issues** | **List[str]** |  | 

## Example

```python
from spearmint_sdk.models.balance_report_response import BalanceReportResponse

# TODO update the JSON string below
json = "{}"
# create an instance of BalanceReportResponse from a JSON string
balance_report_response_instance = BalanceReportResponse.from_json(json)
# print the JSON string representation of the object
print(BalanceReportResponse.to_json())

# convert the object into a dict
balance_report_response_dict = balance_report_response_instance.to_dict()
# create an instance of BalanceReportResponse from a dict
balance_report_response_from_dict = BalanceReportResponse.from_dict(balance_report_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


