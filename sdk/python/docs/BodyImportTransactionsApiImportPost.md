# BodyImportTransactionsApiImportPost


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**file** | **bytearray** | Excel file to import | 
**mode** | **str** | Import mode | [optional] [default to 'incremental']
**skip_duplicates** | **bool** | Skip duplicate transactions | [optional] [default to True]

## Example

```python
from spearmint_sdk.models.body_import_transactions_api_import_post import BodyImportTransactionsApiImportPost

# TODO update the JSON string below
json = "{}"
# create an instance of BodyImportTransactionsApiImportPost from a JSON string
body_import_transactions_api_import_post_instance = BodyImportTransactionsApiImportPost.from_json(json)
# print the JSON string representation of the object
print(BodyImportTransactionsApiImportPost.to_json())

# convert the object into a dict
body_import_transactions_api_import_post_dict = body_import_transactions_api_import_post_instance.to_dict()
# create an instance of BodyImportTransactionsApiImportPost from a dict
body_import_transactions_api_import_post_from_dict = BodyImportTransactionsApiImportPost.from_dict(body_import_transactions_api_import_post_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


