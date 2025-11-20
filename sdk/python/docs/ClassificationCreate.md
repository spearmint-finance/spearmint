# ClassificationCreate

Schema for creating a new classification.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**classification_name** | **str** | Name of the classification | 
**classification_code** | **str** | Unique code for the classification | 
**description** | **str** |  | [optional] 
**exclude_from_income_calc** | **bool** | Exclude from income calculations | [optional] [default to False]
**exclude_from_expense_calc** | **bool** | Exclude from expense calculations | [optional] [default to False]
**exclude_from_cashflow_calc** | **bool** | Exclude from cash flow calculations | [optional] [default to False]

## Example

```python
from spearmint_sdk.models.classification_create import ClassificationCreate

# TODO update the JSON string below
json = "{}"
# create an instance of ClassificationCreate from a JSON string
classification_create_instance = ClassificationCreate.from_json(json)
# print the JSON string representation of the object
print(ClassificationCreate.to_json())

# convert the object into a dict
classification_create_dict = classification_create_instance.to_dict()
# create an instance of ClassificationCreate from a dict
classification_create_from_dict = ClassificationCreate.from_dict(classification_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


