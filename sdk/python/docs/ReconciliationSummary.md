# ReconciliationSummary

Summary for reconciliation report.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total_income** | **float** | Total income (all transactions) | 
**total_expenses** | **float** | Total expenses (all transactions) | 
**net_cashflow** | **float** | Net cash flow | 
**transaction_count** | **int** | Total number of transactions | 

## Example

```python
from spearmint_sdk.models.reconciliation_summary import ReconciliationSummary

# TODO update the JSON string below
json = "{}"
# create an instance of ReconciliationSummary from a JSON string
reconciliation_summary_instance = ReconciliationSummary.from_json(json)
# print the JSON string representation of the object
print(ReconciliationSummary.to_json())

# convert the object into a dict
reconciliation_summary_dict = reconciliation_summary_instance.to_dict()
# create an instance of ReconciliationSummary from a dict
reconciliation_summary_from_dict = ReconciliationSummary.from_dict(reconciliation_summary_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


