# IncomeDetailReportResponse

Response for detailed income report.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**report_type** | **str** | Type of report | 
**period** | [**ReportPeriod**](ReportPeriod.md) | Report period | 
**mode** | **str** | Analysis mode used | 
**total_income** | **float** | Total income | 
**transaction_count** | **int** | Number of transactions | 
**average_transaction** | **float** | Average transaction amount | 
**categories** | [**List[CategoryDetail]**](CategoryDetail.md) | Income by category | 

## Example

```python
from spearmint_sdk.models.income_detail_report_response import IncomeDetailReportResponse

# TODO update the JSON string below
json = "{}"
# create an instance of IncomeDetailReportResponse from a JSON string
income_detail_report_response_instance = IncomeDetailReportResponse.from_json(json)
# print the JSON string representation of the object
print(IncomeDetailReportResponse.to_json())

# convert the object into a dict
income_detail_report_response_dict = income_detail_report_response_instance.to_dict()
# create an instance of IncomeDetailReportResponse from a dict
income_detail_report_response_from_dict = IncomeDetailReportResponse.from_dict(income_detail_report_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


