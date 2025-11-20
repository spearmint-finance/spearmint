# spearmint_sdk.RelationshipsApi

All URIs are relative to *http://localhost:8000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_relationship_api_relationships_post**](RelationshipsApi.md#create_relationship_api_relationships_post) | **POST** /api/relationships | Create Relationship
[**delete_relationship_api_relationships_relationship_id_delete**](RelationshipsApi.md#delete_relationship_api_relationships_relationship_id_delete) | **DELETE** /api/relationships/{relationship_id} | Delete Relationship
[**detect_all_relationships_api_relationships_detect_all_post**](RelationshipsApi.md#detect_all_relationships_api_relationships_detect_all_post) | **POST** /api/relationships/detect/all | Detect All Relationships
[**detect_credit_card_pairs_api_relationships_detect_credit_cards_post**](RelationshipsApi.md#detect_credit_card_pairs_api_relationships_detect_credit_cards_post) | **POST** /api/relationships/detect/credit-cards | Detect Credit Card Pairs
[**detect_dividend_reinvestment_pairs_api_relationships_detect_dividend_reinvestments_post**](RelationshipsApi.md#detect_dividend_reinvestment_pairs_api_relationships_detect_dividend_reinvestments_post) | **POST** /api/relationships/detect/dividend-reinvestments | Detect Dividend Reinvestment Pairs
[**detect_reimbursement_pairs_api_relationships_detect_reimbursements_post**](RelationshipsApi.md#detect_reimbursement_pairs_api_relationships_detect_reimbursements_post) | **POST** /api/relationships/detect/reimbursements | Detect Reimbursement Pairs
[**detect_transfer_pairs_api_relationships_detect_transfers_post**](RelationshipsApi.md#detect_transfer_pairs_api_relationships_detect_transfers_post) | **POST** /api/relationships/detect/transfers | Detect Transfer Pairs
[**get_related_transactions_api_transactions_transaction_id_relationships_get**](RelationshipsApi.md#get_related_transactions_api_transactions_transaction_id_relationships_get) | **GET** /api/transactions/{transaction_id}/relationships | Get Related Transactions


# **create_relationship_api_relationships_post**
> RelationshipResponse create_relationship_api_relationships_post(relationship_create_request)

Create Relationship

Manually create a relationship between two transactions.

Args:
    request: Relationship creation request
    db: Database session

Returns:
    RelationshipResponse: Created relationship

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.relationship_create_request import RelationshipCreateRequest
from spearmint_sdk.models.relationship_response import RelationshipResponse
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
    api_instance = spearmint_sdk.RelationshipsApi(api_client)
    relationship_create_request = spearmint_sdk.RelationshipCreateRequest() # RelationshipCreateRequest | 

    try:
        # Create Relationship
        api_response = api_instance.create_relationship_api_relationships_post(relationship_create_request)
        print("The response of RelationshipsApi->create_relationship_api_relationships_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RelationshipsApi->create_relationship_api_relationships_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **relationship_create_request** | [**RelationshipCreateRequest**](RelationshipCreateRequest.md)|  | 

### Return type

[**RelationshipResponse**](RelationshipResponse.md)

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

# **delete_relationship_api_relationships_relationship_id_delete**
> SuccessResponse delete_relationship_api_relationships_relationship_id_delete(relationship_id)

Delete Relationship

Delete a relationship between transactions.

Args:
    relationship_id: Relationship ID to delete
    db: Database session

Returns:
    SuccessResponse: Success confirmation

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
    api_instance = spearmint_sdk.RelationshipsApi(api_client)
    relationship_id = 56 # int | 

    try:
        # Delete Relationship
        api_response = api_instance.delete_relationship_api_relationships_relationship_id_delete(relationship_id)
        print("The response of RelationshipsApi->delete_relationship_api_relationships_relationship_id_delete:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RelationshipsApi->delete_relationship_api_relationships_relationship_id_delete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **relationship_id** | **int**|  | 

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

# **detect_all_relationships_api_relationships_detect_all_post**
> DetectAllRelationshipsResponse detect_all_relationships_api_relationships_detect_all_post(auto_link=auto_link, date_tolerance_days=date_tolerance_days)

Detect All Relationships

Run all relationship detection algorithms.

Detects transfer pairs, credit card payments, reimbursements, and dividend reinvestments in a single operation.

Args:
    auto_link: If True, automatically create relationships for high-confidence matches (>=0.8)
    date_tolerance_days: Maximum days between related transactions (for transfers)
    db: Database session

Returns:
    DetectAllRelationshipsResponse: Summary of all detected relationships

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.detect_all_relationships_response import DetectAllRelationshipsResponse
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
    api_instance = spearmint_sdk.RelationshipsApi(api_client)
    auto_link = False # bool | Automatically create relationships for high-confidence matches (optional) (default to False)
    date_tolerance_days = 3 # int | Maximum days between related transactions (optional) (default to 3)

    try:
        # Detect All Relationships
        api_response = api_instance.detect_all_relationships_api_relationships_detect_all_post(auto_link=auto_link, date_tolerance_days=date_tolerance_days)
        print("The response of RelationshipsApi->detect_all_relationships_api_relationships_detect_all_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RelationshipsApi->detect_all_relationships_api_relationships_detect_all_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **auto_link** | **bool**| Automatically create relationships for high-confidence matches | [optional] [default to False]
 **date_tolerance_days** | **int**| Maximum days between related transactions | [optional] [default to 3]

### Return type

[**DetectAllRelationshipsResponse**](DetectAllRelationshipsResponse.md)

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

# **detect_credit_card_pairs_api_relationships_detect_credit_cards_post**
> CreditCardPairsResponse detect_credit_card_pairs_api_relationships_detect_credit_cards_post(date_tolerance_days=date_tolerance_days, auto_link=auto_link)

Detect Credit Card Pairs

Detect credit card payment/receipt pairs.

Identifies matching pairs of credit card payments (from bank account) and
receipts (to credit card company) to prevent double-counting in analysis.

Args:
    date_tolerance_days: Maximum days between payment and receipt (default: 5)
    auto_link: If True, automatically create relationships for high-confidence matches (>=0.8)
    db: Database session
    
Returns:
    CreditCardPairsResponse: Detected credit card pairs with confidence scores

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.credit_card_pairs_response import CreditCardPairsResponse
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
    api_instance = spearmint_sdk.RelationshipsApi(api_client)
    date_tolerance_days = 5 # int | Maximum days between payment and receipt (optional) (default to 5)
    auto_link = False # bool | Automatically create relationships for high-confidence matches (optional) (default to False)

    try:
        # Detect Credit Card Pairs
        api_response = api_instance.detect_credit_card_pairs_api_relationships_detect_credit_cards_post(date_tolerance_days=date_tolerance_days, auto_link=auto_link)
        print("The response of RelationshipsApi->detect_credit_card_pairs_api_relationships_detect_credit_cards_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RelationshipsApi->detect_credit_card_pairs_api_relationships_detect_credit_cards_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **date_tolerance_days** | **int**| Maximum days between payment and receipt | [optional] [default to 5]
 **auto_link** | **bool**| Automatically create relationships for high-confidence matches | [optional] [default to False]

### Return type

[**CreditCardPairsResponse**](CreditCardPairsResponse.md)

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

# **detect_dividend_reinvestment_pairs_api_relationships_detect_dividend_reinvestments_post**
> DividendReinvestmentPairsResponse detect_dividend_reinvestment_pairs_api_relationships_detect_dividend_reinvestments_post(date_tolerance_days=date_tolerance_days, amount_tolerance=amount_tolerance, auto_link=auto_link)

Detect Dividend Reinvestment Pairs

Detect dividend reinvestment pairs (dividend income + automatic reinvestment).

Identifies dividend income transactions that were automatically reinvested
in the same security. Links the dividend (income) with the reinvestment (expense).

Args:
    date_tolerance_days: Maximum days between dividend and reinvestment (default: 1)
    amount_tolerance: Maximum amount difference to consider a match (default: 0.01)
    auto_link: If True, automatically create relationships for high-confidence matches (>=0.8)
    db: Database session

Returns:
    DividendReinvestmentPairsResponse: Detected dividend reinvestment pairs with confidence scores

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.dividend_reinvestment_pairs_response import DividendReinvestmentPairsResponse
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
    api_instance = spearmint_sdk.RelationshipsApi(api_client)
    date_tolerance_days = 1 # int | Maximum days between dividend and reinvestment (optional) (default to 1)
    amount_tolerance = 0.01 # float | Maximum amount difference (optional) (default to 0.01)
    auto_link = False # bool | Automatically create relationships for high-confidence matches (optional) (default to False)

    try:
        # Detect Dividend Reinvestment Pairs
        api_response = api_instance.detect_dividend_reinvestment_pairs_api_relationships_detect_dividend_reinvestments_post(date_tolerance_days=date_tolerance_days, amount_tolerance=amount_tolerance, auto_link=auto_link)
        print("The response of RelationshipsApi->detect_dividend_reinvestment_pairs_api_relationships_detect_dividend_reinvestments_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RelationshipsApi->detect_dividend_reinvestment_pairs_api_relationships_detect_dividend_reinvestments_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **date_tolerance_days** | **int**| Maximum days between dividend and reinvestment | [optional] [default to 1]
 **amount_tolerance** | **float**| Maximum amount difference | [optional] [default to 0.01]
 **auto_link** | **bool**| Automatically create relationships for high-confidence matches | [optional] [default to False]

### Return type

[**DividendReinvestmentPairsResponse**](DividendReinvestmentPairsResponse.md)

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

# **detect_reimbursement_pairs_api_relationships_detect_reimbursements_post**
> ReimbursementPairsResponse detect_reimbursement_pairs_api_relationships_detect_reimbursements_post(date_tolerance_days=date_tolerance_days, auto_link=auto_link)

Detect Reimbursement Pairs

Detect reimbursement pairs (expense paid + reimbursement received).

Identifies expenses that were later reimbursed to properly track
out-of-pocket costs vs. reimbursed amounts.

Args:
    date_tolerance_days: Maximum days between expense and reimbursement (default: 30)
    auto_link: If True, automatically create relationships for high-confidence matches (>=0.8)
    db: Database session
    
Returns:
    ReimbursementPairsResponse: Detected reimbursement pairs with confidence scores

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.reimbursement_pairs_response import ReimbursementPairsResponse
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
    api_instance = spearmint_sdk.RelationshipsApi(api_client)
    date_tolerance_days = 30 # int | Maximum days between expense and reimbursement (optional) (default to 30)
    auto_link = False # bool | Automatically create relationships for high-confidence matches (optional) (default to False)

    try:
        # Detect Reimbursement Pairs
        api_response = api_instance.detect_reimbursement_pairs_api_relationships_detect_reimbursements_post(date_tolerance_days=date_tolerance_days, auto_link=auto_link)
        print("The response of RelationshipsApi->detect_reimbursement_pairs_api_relationships_detect_reimbursements_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RelationshipsApi->detect_reimbursement_pairs_api_relationships_detect_reimbursements_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **date_tolerance_days** | **int**| Maximum days between expense and reimbursement | [optional] [default to 30]
 **auto_link** | **bool**| Automatically create relationships for high-confidence matches | [optional] [default to False]

### Return type

[**ReimbursementPairsResponse**](ReimbursementPairsResponse.md)

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

# **detect_transfer_pairs_api_relationships_detect_transfers_post**
> TransferPairsResponse detect_transfer_pairs_api_relationships_detect_transfers_post(date_tolerance_days=date_tolerance_days, amount_tolerance=amount_tolerance, auto_link=auto_link)

Detect Transfer Pairs

Detect potential transfer pairs (same amount, within date range).

Transfer pairs are transactions that represent money moving between accounts,
such as transfers from checking to savings or between different banks.

Args:
    date_tolerance_days: Maximum days between transactions (default: 3)
    amount_tolerance: Maximum amount difference to consider a match (default: 0.01)
    auto_link: If True, automatically create relationships for high-confidence matches (>=0.8)
    db: Database session
    
Returns:
    TransferPairsResponse: Detected transfer pairs with confidence scores

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.transfer_pairs_response import TransferPairsResponse
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
    api_instance = spearmint_sdk.RelationshipsApi(api_client)
    date_tolerance_days = 3 # int | Maximum days between transactions (optional) (default to 3)
    amount_tolerance = 0.01 # float | Maximum amount difference (optional) (default to 0.01)
    auto_link = False # bool | Automatically create relationships for high-confidence matches (optional) (default to False)

    try:
        # Detect Transfer Pairs
        api_response = api_instance.detect_transfer_pairs_api_relationships_detect_transfers_post(date_tolerance_days=date_tolerance_days, amount_tolerance=amount_tolerance, auto_link=auto_link)
        print("The response of RelationshipsApi->detect_transfer_pairs_api_relationships_detect_transfers_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RelationshipsApi->detect_transfer_pairs_api_relationships_detect_transfers_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **date_tolerance_days** | **int**| Maximum days between transactions | [optional] [default to 3]
 **amount_tolerance** | **float**| Maximum amount difference | [optional] [default to 0.01]
 **auto_link** | **bool**| Automatically create relationships for high-confidence matches | [optional] [default to False]

### Return type

[**TransferPairsResponse**](TransferPairsResponse.md)

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

# **get_related_transactions_api_transactions_transaction_id_relationships_get**
> RelatedTransactionsResponse get_related_transactions_api_transactions_transaction_id_relationships_get(transaction_id)

Get Related Transactions

Get all transactions related to a given transaction.

Args:
    transaction_id: Transaction ID
    db: Database session

Returns:
    RelatedTransactionsResponse: Related transactions with relationship info

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.related_transactions_response import RelatedTransactionsResponse
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
    api_instance = spearmint_sdk.RelationshipsApi(api_client)
    transaction_id = 56 # int | 

    try:
        # Get Related Transactions
        api_response = api_instance.get_related_transactions_api_transactions_transaction_id_relationships_get(transaction_id)
        print("The response of RelationshipsApi->get_related_transactions_api_transactions_transaction_id_relationships_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RelationshipsApi->get_related_transactions_api_transactions_transaction_id_relationships_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **transaction_id** | **int**|  | 

### Return type

[**RelatedTransactionsResponse**](RelatedTransactionsResponse.md)

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

