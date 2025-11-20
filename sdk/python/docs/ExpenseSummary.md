# ExpenseSummary

Expense summary in a report.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total** | **float** | Total expenses | 
**transaction_count** | **int** | Number of expense transactions | 
**average_transaction** | **float** | Average expense transaction | 
**top_categories** | [**List[CategorySummary]**](CategorySummary.md) | Top 5 expense categories | 

## Example

```python
from spearmint_sdk.models.expense_summary import ExpenseSummary

# TODO update the JSON string below
json = "{}"
# create an instance of ExpenseSummary from a JSON string
expense_summary_instance = ExpenseSummary.from_json(json)
# print the JSON string representation of the object
print(ExpenseSummary.to_json())

# convert the object into a dict
expense_summary_dict = expense_summary_instance.to_dict()
# create an instance of ExpenseSummary from a dict
expense_summary_from_dict = ExpenseSummary.from_dict(expense_summary_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


