# spearmint_sdk.ReportsApi

All URIs are relative to *http://localhost:8000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_balance_report_api_reports_balances_get**](ReportsApi.md#get_balance_report_api_reports_balances_get) | **GET** /api/reports/balances | Generate Balance Sheet / Net Worth Report
[**get_expense_detail_report_api_reports_expenses_get**](ReportsApi.md#get_expense_detail_report_api_reports_expenses_get) | **GET** /api/reports/expenses | Generate Expense Detail Report
[**get_income_detail_report_api_reports_income_get**](ReportsApi.md#get_income_detail_report_api_reports_income_get) | **GET** /api/reports/income | Generate Income Detail Report
[**get_reconciliation_report_api_reports_reconciliation_get**](ReportsApi.md#get_reconciliation_report_api_reports_reconciliation_get) | **GET** /api/reports/reconciliation | Generate Reconciliation Report
[**get_summary_report_api_reports_summary_get**](ReportsApi.md#get_summary_report_api_reports_summary_get) | **GET** /api/reports/summary | Generate Summary Report


# **get_balance_report_api_reports_balances_get**
> BalanceReportResponse get_balance_report_api_reports_balances_get()

Generate Balance Sheet / Net Worth Report

Generate a report of all account balances and net worth.

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.balance_report_response import BalanceReportResponse
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
    api_instance = spearmint_sdk.ReportsApi(api_client)

    try:
        # Generate Balance Sheet / Net Worth Report
        api_response = api_instance.get_balance_report_api_reports_balances_get()
        print("The response of ReportsApi->get_balance_report_api_reports_balances_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReportsApi->get_balance_report_api_reports_balances_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**BalanceReportResponse**](BalanceReportResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_expense_detail_report_api_reports_expenses_get**
> ExpenseDetailReportResponse get_expense_detail_report_api_reports_expenses_get(start_date=start_date, end_date=end_date, mode=mode, format=format)

Generate Expense Detail Report

Generate a detailed expense report showing:
    - Total expenses for the period
    - Transaction count and averages
    - Complete breakdown by category with percentages
    
    Useful for understanding spending patterns and identifying areas for optimization.

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.expense_detail_report_response import ExpenseDetailReportResponse
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
    api_instance = spearmint_sdk.ReportsApi(api_client)
    start_date = '2013-10-20' # date | Start date (default: 30 days ago) (optional)
    end_date = '2013-10-20' # date | End date (default: today) (optional)
    mode = spearmint_sdk.SrcFinancialAnalysisApiSchemasReportAnalysisModeEnum() # SrcFinancialAnalysisApiSchemasReportAnalysisModeEnum | Analysis mode: 'analysis' excludes transfers, 'complete' includes all (optional)
    format = spearmint_sdk.ReportFormatEnum() # ReportFormatEnum | Export format: 'json' or 'csv' (optional)

    try:
        # Generate Expense Detail Report
        api_response = api_instance.get_expense_detail_report_api_reports_expenses_get(start_date=start_date, end_date=end_date, mode=mode, format=format)
        print("The response of ReportsApi->get_expense_detail_report_api_reports_expenses_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReportsApi->get_expense_detail_report_api_reports_expenses_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **start_date** | **date**| Start date (default: 30 days ago) | [optional] 
 **end_date** | **date**| End date (default: today) | [optional] 
 **mode** | [**SrcFinancialAnalysisApiSchemasReportAnalysisModeEnum**](.md)| Analysis mode: &#39;analysis&#39; excludes transfers, &#39;complete&#39; includes all | [optional] 
 **format** | [**ReportFormatEnum**](.md)| Export format: &#39;json&#39; or &#39;csv&#39; | [optional] 

### Return type

[**ExpenseDetailReportResponse**](ExpenseDetailReportResponse.md)

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

# **get_income_detail_report_api_reports_income_get**
> IncomeDetailReportResponse get_income_detail_report_api_reports_income_get(start_date=start_date, end_date=end_date, mode=mode, format=format)

Generate Income Detail Report

Generate a detailed income report showing:
    - Total income for the period
    - Transaction count and averages
    - Complete breakdown by category with percentages
    
    Useful for understanding income sources and patterns.

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.income_detail_report_response import IncomeDetailReportResponse
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
    api_instance = spearmint_sdk.ReportsApi(api_client)
    start_date = '2013-10-20' # date | Start date (default: 30 days ago) (optional)
    end_date = '2013-10-20' # date | End date (default: today) (optional)
    mode = spearmint_sdk.SrcFinancialAnalysisApiSchemasReportAnalysisModeEnum() # SrcFinancialAnalysisApiSchemasReportAnalysisModeEnum | Analysis mode: 'analysis' excludes transfers, 'complete' includes all (optional)
    format = spearmint_sdk.ReportFormatEnum() # ReportFormatEnum | Export format: 'json' or 'csv' (optional)

    try:
        # Generate Income Detail Report
        api_response = api_instance.get_income_detail_report_api_reports_income_get(start_date=start_date, end_date=end_date, mode=mode, format=format)
        print("The response of ReportsApi->get_income_detail_report_api_reports_income_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReportsApi->get_income_detail_report_api_reports_income_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **start_date** | **date**| Start date (default: 30 days ago) | [optional] 
 **end_date** | **date**| End date (default: today) | [optional] 
 **mode** | [**SrcFinancialAnalysisApiSchemasReportAnalysisModeEnum**](.md)| Analysis mode: &#39;analysis&#39; excludes transfers, &#39;complete&#39; includes all | [optional] 
 **format** | [**ReportFormatEnum**](.md)| Export format: &#39;json&#39; or &#39;csv&#39; | [optional] 

### Return type

[**IncomeDetailReportResponse**](IncomeDetailReportResponse.md)

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

# **get_reconciliation_report_api_reports_reconciliation_get**
> ReconciliationReportResponse get_reconciliation_report_api_reports_reconciliation_get(start_date=start_date, end_date=end_date, format=format)

Generate Reconciliation Report

Generate a reconciliation report showing ALL transactions including transfers.
    
    This report uses COMPLETE mode to show:
    - All transactions in the period (including transfers, credit card payments, etc.)
    - Complete transaction details for reconciliation
    - Summary statistics
    
    Useful for:
    - Bank reconciliation
    - Verifying all transactions are accounted for
    - Auditing purposes
    - Complete financial picture

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.reconciliation_report_response import ReconciliationReportResponse
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
    api_instance = spearmint_sdk.ReportsApi(api_client)
    start_date = '2013-10-20' # date | Start date (default: 30 days ago) (optional)
    end_date = '2013-10-20' # date | End date (default: today) (optional)
    format = spearmint_sdk.ReportFormatEnum() # ReportFormatEnum | Export format: 'json' or 'csv' (optional)

    try:
        # Generate Reconciliation Report
        api_response = api_instance.get_reconciliation_report_api_reports_reconciliation_get(start_date=start_date, end_date=end_date, format=format)
        print("The response of ReportsApi->get_reconciliation_report_api_reports_reconciliation_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReportsApi->get_reconciliation_report_api_reports_reconciliation_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **start_date** | **date**| Start date (default: 30 days ago) | [optional] 
 **end_date** | **date**| End date (default: today) | [optional] 
 **format** | [**ReportFormatEnum**](.md)| Export format: &#39;json&#39; or &#39;csv&#39; | [optional] 

### Return type

[**ReconciliationReportResponse**](ReconciliationReportResponse.md)

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

# **get_summary_report_api_reports_summary_get**
> SummaryReportResponse get_summary_report_api_reports_summary_get(start_date=start_date, end_date=end_date, mode=mode, format=format)

Generate Summary Report

Generate a comprehensive financial summary report including:
    - Income summary with top categories
    - Expense summary with top categories
    - Cash flow summary
    - Financial health indicators
    
    The report can be generated in JSON or CSV format.

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.summary_report_response import SummaryReportResponse
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
    api_instance = spearmint_sdk.ReportsApi(api_client)
    start_date = '2013-10-20' # date | Start date (default: 30 days ago) (optional)
    end_date = '2013-10-20' # date | End date (default: today) (optional)
    mode = spearmint_sdk.SrcFinancialAnalysisApiSchemasReportAnalysisModeEnum() # SrcFinancialAnalysisApiSchemasReportAnalysisModeEnum | Analysis mode: 'analysis' excludes transfers, 'complete' includes all (optional)
    format = spearmint_sdk.ReportFormatEnum() # ReportFormatEnum | Export format: 'json' or 'csv' (optional)

    try:
        # Generate Summary Report
        api_response = api_instance.get_summary_report_api_reports_summary_get(start_date=start_date, end_date=end_date, mode=mode, format=format)
        print("The response of ReportsApi->get_summary_report_api_reports_summary_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReportsApi->get_summary_report_api_reports_summary_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **start_date** | **date**| Start date (default: 30 days ago) | [optional] 
 **end_date** | **date**| End date (default: today) | [optional] 
 **mode** | [**SrcFinancialAnalysisApiSchemasReportAnalysisModeEnum**](.md)| Analysis mode: &#39;analysis&#39; excludes transfers, &#39;complete&#39; includes all | [optional] 
 **format** | [**ReportFormatEnum**](.md)| Export format: &#39;json&#39; or &#39;csv&#39; | [optional] 

### Return type

[**SummaryReportResponse**](SummaryReportResponse.md)

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

