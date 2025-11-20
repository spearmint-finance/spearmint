# ClassificationUpdate

Schema for updating a classification.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**classification_name** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**exclude_from_income_calc** | **bool** |  | [optional] 
**exclude_from_expense_calc** | **bool** |  | [optional] 
**exclude_from_cashflow_calc** | **bool** |  | [optional] 

## Example

```python
from spearmint_sdk.models.classification_update import ClassificationUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of ClassificationUpdate from a JSON string
classification_update_instance = ClassificationUpdate.from_json(json)
# print the JSON string representation of the object
print(ClassificationUpdate.to_json())

# convert the object into a dict
classification_update_dict = classification_update_instance.to_dict()
# create an instance of ClassificationUpdate from a dict
classification_update_from_dict = ClassificationUpdate.from_dict(classification_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


