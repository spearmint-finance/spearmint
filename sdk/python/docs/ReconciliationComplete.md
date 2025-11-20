# ReconciliationComplete

Schema for completing a reconciliation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**reconciled_by** | **str** |  | [optional] 
**cleared_transaction_ids** | **List[int]** |  | [optional] 

## Example

```python
from spearmint_sdk.models.reconciliation_complete import ReconciliationComplete

# TODO update the JSON string below
json = "{}"
# create an instance of ReconciliationComplete from a JSON string
reconciliation_complete_instance = ReconciliationComplete.from_json(json)
# print the JSON string representation of the object
print(ReconciliationComplete.to_json())

# convert the object into a dict
reconciliation_complete_dict = reconciliation_complete_instance.to_dict()
# create an instance of ReconciliationComplete from a dict
reconciliation_complete_from_dict = ReconciliationComplete.from_dict(reconciliation_complete_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


