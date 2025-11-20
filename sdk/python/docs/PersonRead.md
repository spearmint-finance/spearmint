# PersonRead

Schema returned for a person.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**person_id** | **int** |  | 
**name** | **str** |  | 
**is_active** | **bool** |  | 
**created_at** | **datetime** |  | 

## Example

```python
from spearmint_sdk.models.person_read import PersonRead

# TODO update the JSON string below
json = "{}"
# create an instance of PersonRead from a JSON string
person_read_instance = PersonRead.from_json(json)
# print the JSON string representation of the object
print(PersonRead.to_json())

# convert the object into a dict
person_read_dict = person_read_instance.to_dict()
# create an instance of PersonRead from a dict
person_read_from_dict = PersonRead.from_dict(person_read_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


