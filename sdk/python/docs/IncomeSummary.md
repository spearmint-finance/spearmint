# IncomeSummary

Income summary in a report.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total** | **float** | Total income | 
**transaction_count** | **int** | Number of income transactions | 
**average_transaction** | **float** | Average income transaction | 
**top_categories** | [**List[CategorySummary]**](CategorySummary.md) | Top 5 income categories | 

## Example

```python
from spearmint_sdk.models.income_summary import IncomeSummary

# TODO update the JSON string below
json = "{}"
# create an instance of IncomeSummary from a JSON string
income_summary_instance = IncomeSummary.from_json(json)
# print the JSON string representation of the object
print(IncomeSummary.to_json())

# convert the object into a dict
income_summary_dict = income_summary_instance.to_dict()
# create an instance of IncomeSummary from a dict
income_summary_from_dict = IncomeSummary.from_dict(income_summary_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


