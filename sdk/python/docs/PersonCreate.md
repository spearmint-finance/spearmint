# PersonCreate

Schema to create a person.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**is_active** | **bool** |  | [optional] [default to True]

## Example

```python
from spearmint_sdk.models.person_create import PersonCreate

# TODO update the JSON string below
json = "{}"
# create an instance of PersonCreate from a JSON string
person_create_instance = PersonCreate.from_json(json)
# print the JSON string representation of the object
print(PersonCreate.to_json())

# convert the object into a dict
person_create_dict = person_create_instance.to_dict()
# create an instance of PersonCreate from a dict
person_create_from_dict = PersonCreate.from_dict(person_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


