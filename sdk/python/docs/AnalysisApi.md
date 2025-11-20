# spearmint_sdk.AnalysisApi

All URIs are relative to *http://localhost:8000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_cash_flow_analysis_api_analysis_cashflow_get**](AnalysisApi.md#get_cash_flow_analysis_api_analysis_cashflow_get) | **GET** /api/analysis/cashflow | Get Cash Flow Analysis
[**get_cash_flow_trends_api_analysis_cashflow_trends_get**](AnalysisApi.md#get_cash_flow_trends_api_analysis_cashflow_trends_get) | **GET** /api/analysis/cashflow/trends | Get Cash Flow Trends
[**get_category_breakdown_api_analysis_category_breakdown_get**](AnalysisApi.md#get_category_breakdown_api_analysis_category_breakdown_get) | **GET** /api/analysis/category-breakdown | Get Category Breakdown
[**get_expense_analysis_api_analysis_expenses_get**](AnalysisApi.md#get_expense_analysis_api_analysis_expenses_get) | **GET** /api/analysis/expenses | Get Expense Analysis
[**get_expense_category_trends_api_analysis_expenses_category_trends_get**](AnalysisApi.md#get_expense_category_trends_api_analysis_expenses_category_trends_get) | **GET** /api/analysis/expenses/category-trends | Get Expense Category Trends
[**get_expense_trends_api_analysis_expenses_trends_get**](AnalysisApi.md#get_expense_trends_api_analysis_expenses_trends_get) | **GET** /api/analysis/expenses/trends | Get Expense Trends
[**get_financial_health_api_analysis_health_get**](AnalysisApi.md#get_financial_health_api_analysis_health_get) | **GET** /api/analysis/health | Get Financial Health
[**get_financial_summary_api_analysis_summary_get**](AnalysisApi.md#get_financial_summary_api_analysis_summary_get) | **GET** /api/analysis/summary | Get Financial Summary
[**get_income_analysis_api_analysis_income_get**](AnalysisApi.md#get_income_analysis_api_analysis_income_get) | **GET** /api/analysis/income | Get Income Analysis
[**get_income_expense_comparison_api_analysis_income_expense_get**](AnalysisApi.md#get_income_expense_comparison_api_analysis_income_expense_get) | **GET** /api/analysis/income-expense | Get Income Expense Comparison
[**get_income_trends_api_analysis_income_trends_get**](AnalysisApi.md#get_income_trends_api_analysis_income_trends_get) | **GET** /api/analysis/income/trends | Get Income Trends


# **get_cash_flow_analysis_api_analysis_cashflow_get**
> CashFlowResponse get_cash_flow_analysis_api_analysis_cashflow_get(start_date=start_date, end_date=end_date, mode=mode)

Get Cash Flow Analysis

Get cash flow analysis for a period.

Args:
    start_date: Start date for analysis
    end_date: End date for analysis
    mode: Analysis mode (analysis or complete)
    db: Database session
    
Returns:
    CashFlowResponse: Cash flow analysis results

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.cash_flow_response import CashFlowResponse
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
    api_instance = spearmint_sdk.AnalysisApi(api_client)
    start_date = '2013-10-20' # date | Start date for analysis (optional)
    end_date = '2013-10-20' # date | End date for analysis (optional)
    mode = spearmint_sdk.SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum() # SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum | Analysis mode (optional)

    try:
        # Get Cash Flow Analysis
        api_response = api_instance.get_cash_flow_analysis_api_analysis_cashflow_get(start_date=start_date, end_date=end_date, mode=mode)
        print("The response of AnalysisApi->get_cash_flow_analysis_api_analysis_cashflow_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AnalysisApi->get_cash_flow_analysis_api_analysis_cashflow_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **start_date** | **date**| Start date for analysis | [optional] 
 **end_date** | **date**| End date for analysis | [optional] 
 **mode** | [**SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum**](.md)| Analysis mode | [optional] 

### Return type

[**CashFlowResponse**](CashFlowResponse.md)

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

# **get_cash_flow_trends_api_analysis_cashflow_trends_get**
> CashFlowTrendsResponse get_cash_flow_trends_api_analysis_cashflow_trends_get(start_date=start_date, end_date=end_date, period=period, mode=mode)

Get Cash Flow Trends

Get cash flow trends over time.

Args:
    start_date: Start date for analysis
    end_date: End date for analysis
    period: Period granularity (daily, weekly, monthly, etc.)
    mode: Analysis mode
    db: Database session
    
Returns:
    CashFlowTrendsResponse: Cash flow trend data

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.cash_flow_trends_response import CashFlowTrendsResponse
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
    api_instance = spearmint_sdk.AnalysisApi(api_client)
    start_date = '2013-10-20' # date | Start date for analysis (optional)
    end_date = '2013-10-20' # date | End date for analysis (optional)
    period = spearmint_sdk.TimePeriodEnum() # TimePeriodEnum | Period granularity (optional)
    mode = spearmint_sdk.SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum() # SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum | Analysis mode (optional)

    try:
        # Get Cash Flow Trends
        api_response = api_instance.get_cash_flow_trends_api_analysis_cashflow_trends_get(start_date=start_date, end_date=end_date, period=period, mode=mode)
        print("The response of AnalysisApi->get_cash_flow_trends_api_analysis_cashflow_trends_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AnalysisApi->get_cash_flow_trends_api_analysis_cashflow_trends_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **start_date** | **date**| Start date for analysis | [optional] 
 **end_date** | **date**| End date for analysis | [optional] 
 **period** | [**TimePeriodEnum**](.md)| Period granularity | [optional] 
 **mode** | [**SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum**](.md)| Analysis mode | [optional] 

### Return type

[**CashFlowTrendsResponse**](CashFlowTrendsResponse.md)

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

# **get_category_breakdown_api_analysis_category_breakdown_get**
> CategoryBreakdownResponse get_category_breakdown_api_analysis_category_breakdown_get(start_date=start_date, end_date=end_date, mode=mode)

Get Category Breakdown

Get detailed category breakdown for income and expenses.

This endpoint provides a comprehensive breakdown of all categories including:
- Income categories with totals, counts, and percentages
- Expense categories with totals, counts, and percentages
- Percentage of total for each category type
- Percentage of all transactions

Args:
    start_date: Start date for analysis
    end_date: End date for analysis
    mode: Analysis mode (analysis or complete)
    db: Database session

Returns:
    CategoryBreakdownResponse: Detailed category breakdown

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.category_breakdown_response import CategoryBreakdownResponse
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
    api_instance = spearmint_sdk.AnalysisApi(api_client)
    start_date = '2013-10-20' # date | Start date for analysis (optional)
    end_date = '2013-10-20' # date | End date for analysis (optional)
    mode = spearmint_sdk.SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum() # SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum | Analysis mode (optional)

    try:
        # Get Category Breakdown
        api_response = api_instance.get_category_breakdown_api_analysis_category_breakdown_get(start_date=start_date, end_date=end_date, mode=mode)
        print("The response of AnalysisApi->get_category_breakdown_api_analysis_category_breakdown_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AnalysisApi->get_category_breakdown_api_analysis_category_breakdown_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **start_date** | **date**| Start date for analysis | [optional] 
 **end_date** | **date**| End date for analysis | [optional] 
 **mode** | [**SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum**](.md)| Analysis mode | [optional] 

### Return type

[**CategoryBreakdownResponse**](CategoryBreakdownResponse.md)

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

# **get_expense_analysis_api_analysis_expenses_get**
> ExpenseAnalysisResponse get_expense_analysis_api_analysis_expenses_get(start_date=start_date, end_date=end_date, mode=mode, top_n=top_n)

Get Expense Analysis

Get expense analysis for a period.

Args:
    start_date: Start date for analysis
    end_date: End date for analysis
    mode: Analysis mode (analysis or complete)
    top_n: Number of top categories to return
    db: Database session
    
Returns:
    ExpenseAnalysisResponse: Expense analysis results

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.expense_analysis_response import ExpenseAnalysisResponse
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
    api_instance = spearmint_sdk.AnalysisApi(api_client)
    start_date = '2013-10-20' # date | Start date for analysis (optional)
    end_date = '2013-10-20' # date | End date for analysis (optional)
    mode = spearmint_sdk.SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum() # SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum | Analysis mode (optional)
    top_n = 10 # int | Number of top categories to return (optional) (default to 10)

    try:
        # Get Expense Analysis
        api_response = api_instance.get_expense_analysis_api_analysis_expenses_get(start_date=start_date, end_date=end_date, mode=mode, top_n=top_n)
        print("The response of AnalysisApi->get_expense_analysis_api_analysis_expenses_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AnalysisApi->get_expense_analysis_api_analysis_expenses_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **start_date** | **date**| Start date for analysis | [optional] 
 **end_date** | **date**| End date for analysis | [optional] 
 **mode** | [**SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum**](.md)| Analysis mode | [optional] 
 **top_n** | **int**| Number of top categories to return | [optional] [default to 10]

### Return type

[**ExpenseAnalysisResponse**](ExpenseAnalysisResponse.md)

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

# **get_expense_category_trends_api_analysis_expenses_category_trends_get**
> object get_expense_category_trends_api_analysis_expenses_category_trends_get(start_date=start_date, end_date=end_date, period=period, mode=mode, top_n=top_n)

Get Expense Category Trends

Get expense trends broken down by category for stacked charts.

Returns expense amounts for each category for each time period,
allowing for accurate stacked bar charts that show actual expenses
per period rather than proportional distributions.

### Example


```python
import spearmint_sdk
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
    api_instance = spearmint_sdk.AnalysisApi(api_client)
    start_date = '2013-10-20' # date | Start date for analysis (optional)
    end_date = '2013-10-20' # date | End date for analysis (optional)
    period = spearmint_sdk.TimePeriodEnum() # TimePeriodEnum | Period granularity (optional)
    mode = spearmint_sdk.SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum() # SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum | Analysis mode (optional)
    top_n = 8 # int | Number of top categories to include (optional) (default to 8)

    try:
        # Get Expense Category Trends
        api_response = api_instance.get_expense_category_trends_api_analysis_expenses_category_trends_get(start_date=start_date, end_date=end_date, period=period, mode=mode, top_n=top_n)
        print("The response of AnalysisApi->get_expense_category_trends_api_analysis_expenses_category_trends_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AnalysisApi->get_expense_category_trends_api_analysis_expenses_category_trends_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **start_date** | **date**| Start date for analysis | [optional] 
 **end_date** | **date**| End date for analysis | [optional] 
 **period** | [**TimePeriodEnum**](.md)| Period granularity | [optional] 
 **mode** | [**SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum**](.md)| Analysis mode | [optional] 
 **top_n** | **int**| Number of top categories to include | [optional] [default to 8]

### Return type

**object**

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

# **get_expense_trends_api_analysis_expenses_trends_get**
> TrendsResponse get_expense_trends_api_analysis_expenses_trends_get(start_date=start_date, end_date=end_date, period=period, mode=mode)

Get Expense Trends

Get expense trends over time.

Args:
    start_date: Start date for analysis
    end_date: End date for analysis
    period: Period granularity (daily, weekly, monthly, etc.)
    mode: Analysis mode
    db: Database session
    
Returns:
    TrendsResponse: Expense trend data

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.trends_response import TrendsResponse
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
    api_instance = spearmint_sdk.AnalysisApi(api_client)
    start_date = '2013-10-20' # date | Start date for analysis (optional)
    end_date = '2013-10-20' # date | End date for analysis (optional)
    period = spearmint_sdk.TimePeriodEnum() # TimePeriodEnum | Period granularity (optional)
    mode = spearmint_sdk.SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum() # SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum | Analysis mode (optional)

    try:
        # Get Expense Trends
        api_response = api_instance.get_expense_trends_api_analysis_expenses_trends_get(start_date=start_date, end_date=end_date, period=period, mode=mode)
        print("The response of AnalysisApi->get_expense_trends_api_analysis_expenses_trends_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AnalysisApi->get_expense_trends_api_analysis_expenses_trends_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **start_date** | **date**| Start date for analysis | [optional] 
 **end_date** | **date**| End date for analysis | [optional] 
 **period** | [**TimePeriodEnum**](.md)| Period granularity | [optional] 
 **mode** | [**SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum**](.md)| Analysis mode | [optional] 

### Return type

[**TrendsResponse**](TrendsResponse.md)

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

# **get_financial_health_api_analysis_health_get**
> FinancialHealthResponse get_financial_health_api_analysis_health_get(start_date=start_date, end_date=end_date, mode=mode)

Get Financial Health

Get financial health indicators.

Args:
    start_date: Start date for analysis
    end_date: End date for analysis
    mode: Analysis mode (analysis, with_capital, or complete)
    db: Database session

Returns:
    FinancialHealthResponse: Financial health indicators

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.financial_health_response import FinancialHealthResponse
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
    api_instance = spearmint_sdk.AnalysisApi(api_client)
    start_date = '2013-10-20' # date | Start date for analysis (optional)
    end_date = '2013-10-20' # date | End date for analysis (optional)
    mode = spearmint_sdk.SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum() # SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum | Analysis mode (optional)

    try:
        # Get Financial Health
        api_response = api_instance.get_financial_health_api_analysis_health_get(start_date=start_date, end_date=end_date, mode=mode)
        print("The response of AnalysisApi->get_financial_health_api_analysis_health_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AnalysisApi->get_financial_health_api_analysis_health_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **start_date** | **date**| Start date for analysis | [optional] 
 **end_date** | **date**| End date for analysis | [optional] 
 **mode** | [**SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum**](.md)| Analysis mode | [optional] 

### Return type

[**FinancialHealthResponse**](FinancialHealthResponse.md)

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

# **get_financial_summary_api_analysis_summary_get**
> FinancialSummaryResponse get_financial_summary_api_analysis_summary_get(start_date=start_date, end_date=end_date, mode=mode, top_n=top_n, recent_count=recent_count)

Get Financial Summary

Get comprehensive financial summary.

This endpoint provides a complete financial overview including:
- Total income, expenses, and net cash flow
- Top income and expense categories
- Recent transactions
- Financial health indicators

Args:
    start_date: Start date for analysis
    end_date: End date for analysis
    mode: Analysis mode (analysis or complete)
    top_n: Number of top categories to return
    recent_count: Number of recent transactions to return
    db: Database session

Returns:
    FinancialSummaryResponse: Comprehensive financial summary

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.financial_summary_response import FinancialSummaryResponse
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
    api_instance = spearmint_sdk.AnalysisApi(api_client)
    start_date = '2013-10-20' # date | Start date for analysis (optional)
    end_date = '2013-10-20' # date | End date for analysis (optional)
    mode = spearmint_sdk.SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum() # SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum | Analysis mode (optional)
    top_n = 5 # int | Number of top categories to return (optional) (default to 5)
    recent_count = 10 # int | Number of recent transactions to return (optional) (default to 10)

    try:
        # Get Financial Summary
        api_response = api_instance.get_financial_summary_api_analysis_summary_get(start_date=start_date, end_date=end_date, mode=mode, top_n=top_n, recent_count=recent_count)
        print("The response of AnalysisApi->get_financial_summary_api_analysis_summary_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AnalysisApi->get_financial_summary_api_analysis_summary_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **start_date** | **date**| Start date for analysis | [optional] 
 **end_date** | **date**| End date for analysis | [optional] 
 **mode** | [**SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum**](.md)| Analysis mode | [optional] 
 **top_n** | **int**| Number of top categories to return | [optional] [default to 5]
 **recent_count** | **int**| Number of recent transactions to return | [optional] [default to 10]

### Return type

[**FinancialSummaryResponse**](FinancialSummaryResponse.md)

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

# **get_income_analysis_api_analysis_income_get**
> IncomeAnalysisResponse get_income_analysis_api_analysis_income_get(start_date=start_date, end_date=end_date, mode=mode)

Get Income Analysis

Get income analysis for a period.

Args:
    start_date: Start date for analysis
    end_date: End date for analysis
    mode: Analysis mode (analysis or complete)
    db: Database session
    
Returns:
    IncomeAnalysisResponse: Income analysis results

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.income_analysis_response import IncomeAnalysisResponse
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
    api_instance = spearmint_sdk.AnalysisApi(api_client)
    start_date = '2013-10-20' # date | Start date for analysis (optional)
    end_date = '2013-10-20' # date | End date for analysis (optional)
    mode = spearmint_sdk.SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum() # SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum | Analysis mode (optional)

    try:
        # Get Income Analysis
        api_response = api_instance.get_income_analysis_api_analysis_income_get(start_date=start_date, end_date=end_date, mode=mode)
        print("The response of AnalysisApi->get_income_analysis_api_analysis_income_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AnalysisApi->get_income_analysis_api_analysis_income_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **start_date** | **date**| Start date for analysis | [optional] 
 **end_date** | **date**| End date for analysis | [optional] 
 **mode** | [**SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum**](.md)| Analysis mode | [optional] 

### Return type

[**IncomeAnalysisResponse**](IncomeAnalysisResponse.md)

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

# **get_income_expense_comparison_api_analysis_income_expense_get**
> IncomeExpenseComparisonResponse get_income_expense_comparison_api_analysis_income_expense_get(start_date=start_date, end_date=end_date, mode=mode, top_n=top_n)

Get Income Expense Comparison

Get combined income and expense comparison.

This endpoint provides a side-by-side comparison of income and expenses including:
- Detailed income analysis
- Detailed expense analysis
- Cash flow summary
- Comparison metrics (ratios, percentages)

Args:
    start_date: Start date for analysis
    end_date: End date for analysis
    mode: Analysis mode (analysis or complete)
    top_n: Number of top categories to return
    db: Database session

Returns:
    IncomeExpenseComparisonResponse: Income vs expense comparison

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.income_expense_comparison_response import IncomeExpenseComparisonResponse
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
    api_instance = spearmint_sdk.AnalysisApi(api_client)
    start_date = '2013-10-20' # date | Start date for analysis (optional)
    end_date = '2013-10-20' # date | End date for analysis (optional)
    mode = spearmint_sdk.SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum() # SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum | Analysis mode (optional)
    top_n = 10 # int | Number of top categories to return (optional) (default to 10)

    try:
        # Get Income Expense Comparison
        api_response = api_instance.get_income_expense_comparison_api_analysis_income_expense_get(start_date=start_date, end_date=end_date, mode=mode, top_n=top_n)
        print("The response of AnalysisApi->get_income_expense_comparison_api_analysis_income_expense_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AnalysisApi->get_income_expense_comparison_api_analysis_income_expense_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **start_date** | **date**| Start date for analysis | [optional] 
 **end_date** | **date**| End date for analysis | [optional] 
 **mode** | [**SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum**](.md)| Analysis mode | [optional] 
 **top_n** | **int**| Number of top categories to return | [optional] [default to 10]

### Return type

[**IncomeExpenseComparisonResponse**](IncomeExpenseComparisonResponse.md)

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

# **get_income_trends_api_analysis_income_trends_get**
> TrendsResponse get_income_trends_api_analysis_income_trends_get(start_date=start_date, end_date=end_date, period=period, mode=mode)

Get Income Trends

Get income trends over time.

Args:
    start_date: Start date for analysis
    end_date: End date for analysis
    period: Period granularity (daily, weekly, monthly, etc.)
    mode: Analysis mode
    db: Database session
    
Returns:
    TrendsResponse: Income trend data

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.trends_response import TrendsResponse
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
    api_instance = spearmint_sdk.AnalysisApi(api_client)
    start_date = '2013-10-20' # date | Start date for analysis (optional)
    end_date = '2013-10-20' # date | End date for analysis (optional)
    period = spearmint_sdk.TimePeriodEnum() # TimePeriodEnum | Period granularity (optional)
    mode = spearmint_sdk.SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum() # SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum | Analysis mode (optional)

    try:
        # Get Income Trends
        api_response = api_instance.get_income_trends_api_analysis_income_trends_get(start_date=start_date, end_date=end_date, period=period, mode=mode)
        print("The response of AnalysisApi->get_income_trends_api_analysis_income_trends_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AnalysisApi->get_income_trends_api_analysis_income_trends_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **start_date** | **date**| Start date for analysis | [optional] 
 **end_date** | **date**| End date for analysis | [optional] 
 **period** | [**TimePeriodEnum**](.md)| Period granularity | [optional] 
 **mode** | [**SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum**](.md)| Analysis mode | [optional] 

### Return type

[**TrendsResponse**](TrendsResponse.md)

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

