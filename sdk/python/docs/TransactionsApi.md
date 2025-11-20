# spearmint_sdk.TransactionsApi

All URIs are relative to *http://localhost:8000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_transaction_api_transactions_post**](TransactionsApi.md#create_transaction_api_transactions_post) | **POST** /api/transactions | Create Transaction
[**delete_transaction_api_transactions_transaction_id_delete**](TransactionsApi.md#delete_transaction_api_transactions_transaction_id_delete) | **DELETE** /api/transactions/{transaction_id} | Delete Transaction
[**get_transaction_api_transactions_transaction_id_get**](TransactionsApi.md#get_transaction_api_transactions_transaction_id_get) | **GET** /api/transactions/{transaction_id} | Get Transaction
[**list_transactions_api_transactions_get**](TransactionsApi.md#list_transactions_api_transactions_get) | **GET** /api/transactions | List Transactions
[**update_transaction_api_transactions_transaction_id_put**](TransactionsApi.md#update_transaction_api_transactions_transaction_id_put) | **PUT** /api/transactions/{transaction_id} | Update Transaction


# **create_transaction_api_transactions_post**
> TransactionResponse create_transaction_api_transactions_post(transaction_create)

Create Transaction

Create a new transaction.

Args:
    transaction: Transaction data
    db: Database session
    
Returns:
    TransactionResponse: Created transaction

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.transaction_create import TransactionCreate
from spearmint_sdk.models.transaction_response import TransactionResponse
from spearmint_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = spearmint_sdk.Configuration(
    host = "http://localhost:8000"
)


# Enter a context with an instance of the API client
with spearmint_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = spearmint_sdk.TransactionsApi(api_client)
    transaction_create = spearmint_sdk.TransactionCreate() # TransactionCreate | 

    try:
        # Create Transaction
        api_response = api_instance.create_transaction_api_transactions_post(transaction_create)
        print("The response of TransactionsApi->create_transaction_api_transactions_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TransactionsApi->create_transaction_api_transactions_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **transaction_create** | [**TransactionCreate**](TransactionCreate.md)|  | 

### Return type

[**TransactionResponse**](TransactionResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_transaction_api_transactions_transaction_id_delete**
> SuccessResponse delete_transaction_api_transactions_transaction_id_delete(transaction_id)

Delete Transaction

Delete transaction.

Args:
    transaction_id: Transaction ID
    db: Database session
    
Returns:
    SuccessResponse: Success message

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.success_response import SuccessResponse
from spearmint_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = spearmint_sdk.Configuration(
    host = "http://localhost:8000"
)


# Enter a context with an instance of the API client
with spearmint_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = spearmint_sdk.TransactionsApi(api_client)
    transaction_id = 56 # int | 

    try:
        # Delete Transaction
        api_response = api_instance.delete_transaction_api_transactions_transaction_id_delete(transaction_id)
        print("The response of TransactionsApi->delete_transaction_api_transactions_transaction_id_delete:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TransactionsApi->delete_transaction_api_transactions_transaction_id_delete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **transaction_id** | **int**|  | 

### Return type

[**SuccessResponse**](SuccessResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_transaction_api_transactions_transaction_id_get**
> TransactionResponse get_transaction_api_transactions_transaction_id_get(transaction_id)

Get Transaction

Get transaction by ID.

Args:
    transaction_id: Transaction ID
    db: Database session
    
Returns:
    TransactionResponse: Transaction data

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.transaction_response import TransactionResponse
from spearmint_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = spearmint_sdk.Configuration(
    host = "http://localhost:8000"
)


# Enter a context with an instance of the API client
with spearmint_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = spearmint_sdk.TransactionsApi(api_client)
    transaction_id = 56 # int | 

    try:
        # Get Transaction
        api_response = api_instance.get_transaction_api_transactions_transaction_id_get(transaction_id)
        print("The response of TransactionsApi->get_transaction_api_transactions_transaction_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TransactionsApi->get_transaction_api_transactions_transaction_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **transaction_id** | **int**|  | 

### Return type

[**TransactionResponse**](TransactionResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_transactions_api_transactions_get**
> TransactionListResponse list_transactions_api_transactions_get(start_date=start_date, end_date=end_date, transaction_type=transaction_type, category_id=category_id, classification_id=classification_id, include_in_analysis=include_in_analysis, is_transfer=is_transfer, min_amount=min_amount, max_amount=max_amount, search_text=search_text, include_capital_expenses=include_capital_expenses, include_transfers=include_transfers, limit=limit, offset=offset, sort_by=sort_by, sort_order=sort_order)

List Transactions

List transactions with optional filters.

Args:
    Various filter parameters
    db: Database session

Returns:
    TransactionListResponse: List of transactions

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.transaction_list_response import TransactionListResponse
from spearmint_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = spearmint_sdk.Configuration(
    host = "http://localhost:8000"
)


# Enter a context with an instance of the API client
with spearmint_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = spearmint_sdk.TransactionsApi(api_client)
    start_date = '2013-10-20' # date | Start date filter (optional)
    end_date = '2013-10-20' # date | End date filter (optional)
    transaction_type = 'transaction_type_example' # str | Transaction type filter (optional)
    category_id = 56 # int | Category ID filter (optional)
    classification_id = 56 # int | Classification ID filter (optional)
    include_in_analysis = True # bool | Include in analysis filter (optional)
    is_transfer = True # bool | Is transfer filter (optional)
    min_amount = spearmint_sdk.MinAmount() # MinAmount | Minimum amount filter (optional)
    max_amount = spearmint_sdk.MaxAmount() # MaxAmount | Maximum amount filter (optional)
    search_text = 'search_text_example' # str | Search in description, source, notes (optional)
    include_capital_expenses = True # bool | Include non-operating expenses (capital, refunds, reimbursements, etc.) in results (optional) (default to True)
    include_transfers = True # bool | Include transfers in results (optional) (default to True)
    limit = 100 # int | Maximum number of results (optional) (default to 100)
    offset = 0 # int | Number of results to skip (optional) (default to 0)
    sort_by = 'transaction_date' # str | Field to sort by (optional) (default to 'transaction_date')
    sort_order = 'desc' # str | Sort order (optional) (default to 'desc')

    try:
        # List Transactions
        api_response = api_instance.list_transactions_api_transactions_get(start_date=start_date, end_date=end_date, transaction_type=transaction_type, category_id=category_id, classification_id=classification_id, include_in_analysis=include_in_analysis, is_transfer=is_transfer, min_amount=min_amount, max_amount=max_amount, search_text=search_text, include_capital_expenses=include_capital_expenses, include_transfers=include_transfers, limit=limit, offset=offset, sort_by=sort_by, sort_order=sort_order)
        print("The response of TransactionsApi->list_transactions_api_transactions_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TransactionsApi->list_transactions_api_transactions_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **start_date** | **date**| Start date filter | [optional] 
 **end_date** | **date**| End date filter | [optional] 
 **transaction_type** | **str**| Transaction type filter | [optional] 
 **category_id** | **int**| Category ID filter | [optional] 
 **classification_id** | **int**| Classification ID filter | [optional] 
 **include_in_analysis** | **bool**| Include in analysis filter | [optional] 
 **is_transfer** | **bool**| Is transfer filter | [optional] 
 **min_amount** | [**MinAmount**](.md)| Minimum amount filter | [optional] 
 **max_amount** | [**MaxAmount**](.md)| Maximum amount filter | [optional] 
 **search_text** | **str**| Search in description, source, notes | [optional] 
 **include_capital_expenses** | **bool**| Include non-operating expenses (capital, refunds, reimbursements, etc.) in results | [optional] [default to True]
 **include_transfers** | **bool**| Include transfers in results | [optional] [default to True]
 **limit** | **int**| Maximum number of results | [optional] [default to 100]
 **offset** | **int**| Number of results to skip | [optional] [default to 0]
 **sort_by** | **str**| Field to sort by | [optional] [default to &#39;transaction_date&#39;]
 **sort_order** | **str**| Sort order | [optional] [default to &#39;desc&#39;]

### Return type

[**TransactionListResponse**](TransactionListResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_transaction_api_transactions_transaction_id_put**
> TransactionResponse update_transaction_api_transactions_transaction_id_put(transaction_id, transaction_update, reapply_rules=reapply_rules)

Update Transaction

Update transaction.

Args:
    transaction_id: Transaction ID
    transaction: Updated transaction data
    db: Database session
    
Returns:
    TransactionResponse: Updated transaction

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.transaction_response import TransactionResponse
from spearmint_sdk.models.transaction_update import TransactionUpdate
from spearmint_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = spearmint_sdk.Configuration(
    host = "http://localhost:8000"
)


# Enter a context with an instance of the API client
with spearmint_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = spearmint_sdk.TransactionsApi(api_client)
    transaction_id = 56 # int | 
    transaction_update = spearmint_sdk.TransactionUpdate() # TransactionUpdate | 
    reapply_rules = True # bool | If true, re-apply classification rules (optional)

    try:
        # Update Transaction
        api_response = api_instance.update_transaction_api_transactions_transaction_id_put(transaction_id, transaction_update, reapply_rules=reapply_rules)
        print("The response of TransactionsApi->update_transaction_api_transactions_transaction_id_put:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TransactionsApi->update_transaction_api_transactions_transaction_id_put: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **transaction_id** | **int**|  | 
 **transaction_update** | [**TransactionUpdate**](TransactionUpdate.md)|  | 
 **reapply_rules** | **bool**| If true, re-apply classification rules | [optional] 

### Return type

[**TransactionResponse**](TransactionResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

