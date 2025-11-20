# ExpenseDetailReportResponse

Response for detailed expense report.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**report_type** | **str** | Type of report | 
**period** | [**ReportPeriod**](ReportPeriod.md) | Report period | 
**mode** | **str** | Analysis mode used | 
**total_expenses** | **float** | Total expenses | 
**transaction_count** | **int** | Number of transactions | 
**average_transaction** | **float** | Average transaction amount | 
**categories** | [**List[CategoryDetail]**](CategoryDetail.md) | Expenses by category | 

## Example

```python
from spearmint_sdk.models.expense_detail_report_response import ExpenseDetailReportResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ExpenseDetailReportResponse from a JSON string
expense_detail_report_response_instance = ExpenseDetailReportResponse.from_json(json)
# print the JSON string representation of the object
print(ExpenseDetailReportResponse.to_json())

# convert the object into a dict
expense_detail_report_response_dict = expense_detail_report_response_instance.to_dict()
# create an instance of ExpenseDetailReportResponse from a dict
expense_detail_report_response_from_dict = ExpenseDetailReportResponse.from_dict(expense_detail_report_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


