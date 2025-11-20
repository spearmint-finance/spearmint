# ClassificationResponse

Schema for classification response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**classification_name** | **str** | Name of the classification | 
**classification_code** | **str** | Unique code for the classification | 
**description** | **str** |  | [optional] 
**exclude_from_income_calc** | **bool** | Exclude from income calculations | [optional] [default to False]
**exclude_from_expense_calc** | **bool** | Exclude from expense calculations | [optional] [default to False]
**exclude_from_cashflow_calc** | **bool** | Exclude from cash flow calculations | [optional] [default to False]
**classification_id** | **int** | Classification ID | 
**is_system_classification** | **bool** | Whether this is a system classification | 
**created_at** | **datetime** | Creation timestamp | 
**updated_at** | **datetime** | Last update timestamp | 

## Example

```python
from spearmint_sdk.models.classification_response import ClassificationResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ClassificationResponse from a JSON string
classification_response_instance = ClassificationResponse.from_json(json)
# print the JSON string representation of the object
print(ClassificationResponse.to_json())

# convert the object into a dict
classification_response_dict = classification_response_instance.to_dict()
# create an instance of ClassificationResponse from a dict
classification_response_from_dict = ClassificationResponse.from_dict(classification_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


