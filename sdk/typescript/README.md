# @spearmint-money/sdk@0.1.0

A TypeScript SDK client for the localhost API.

## Usage

First, install the SDK from npm.

```bash
npm install @spearmint-money/sdk --save
```

Next, try it out.


```ts
import {
  Configuration,
  AccountsApi,
} from '@spearmint-money/sdk';
import type { AddBalanceSnapshotApiAccountsAccountIdBalancesPostRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new AccountsApi();

  const body = {
    // number | Account ID
    accountId: 56,
    // BalanceCreate
    balanceCreate: ...,
  } satisfies AddBalanceSnapshotApiAccountsAccountIdBalancesPostRequest;

  try {
    const data = await api.addBalanceSnapshotApiAccountsAccountIdBalancesPost(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```


## Documentation

### API Endpoints

All URIs are relative to *http://localhost:8000*

| Class | Method | HTTP request | Description
| ----- | ------ | ------------ | -------------
*AccountsApi* | [**addBalanceSnapshotApiAccountsAccountIdBalancesPost**](docs/AccountsApi.md#addbalancesnapshotapiaccountsaccountidbalancespost) | **POST** /api/accounts/{account_id}/balances | Add Balance Snapshot
*AccountsApi* | [**addBalanceSnapshotApiAccountsAccountIdBalancesPost_0**](docs/AccountsApi.md#addbalancesnapshotapiaccountsaccountidbalancespost_0) | **POST** /api/accounts/{account_id}/balances | Add Balance Snapshot
*AccountsApi* | [**addHoldingApiAccountsAccountIdHoldingsPost**](docs/AccountsApi.md#addholdingapiaccountsaccountidholdingspost) | **POST** /api/accounts/{account_id}/holdings | Add Holding
*AccountsApi* | [**addHoldingApiAccountsAccountIdHoldingsPost_0**](docs/AccountsApi.md#addholdingapiaccountsaccountidholdingspost_0) | **POST** /api/accounts/{account_id}/holdings | Add Holding
*AccountsApi* | [**clearTransactionsApiAccountsTransactionsClearPost**](docs/AccountsApi.md#cleartransactionsapiaccountstransactionsclearpost) | **POST** /api/accounts/transactions/clear | Clear Transactions
*AccountsApi* | [**clearTransactionsApiAccountsTransactionsClearPost_0**](docs/AccountsApi.md#cleartransactionsapiaccountstransactionsclearpost_0) | **POST** /api/accounts/transactions/clear | Clear Transactions
*AccountsApi* | [**completeReconciliationApiAccountsReconciliationsReconciliationIdCompletePut**](docs/AccountsApi.md#completereconciliationapiaccountsreconciliationsreconciliationidcompleteput) | **PUT** /api/accounts/reconciliations/{reconciliation_id}/complete | Complete Reconciliation
*AccountsApi* | [**completeReconciliationApiAccountsReconciliationsReconciliationIdCompletePut_0**](docs/AccountsApi.md#completereconciliationapiaccountsreconciliationsreconciliationidcompleteput_0) | **PUT** /api/accounts/reconciliations/{reconciliation_id}/complete | Complete Reconciliation
*AccountsApi* | [**createAccountApiAccountsPost**](docs/AccountsApi.md#createaccountapiaccountspost) | **POST** /api/accounts | Create Account
*AccountsApi* | [**createAccountApiAccountsPost_0**](docs/AccountsApi.md#createaccountapiaccountspost_0) | **POST** /api/accounts | Create Account
*AccountsApi* | [**createReconciliationApiAccountsAccountIdReconcilePost**](docs/AccountsApi.md#createreconciliationapiaccountsaccountidreconcilepost) | **POST** /api/accounts/{account_id}/reconcile | Create Reconciliation
*AccountsApi* | [**createReconciliationApiAccountsAccountIdReconcilePost_0**](docs/AccountsApi.md#createreconciliationapiaccountsaccountidreconcilepost_0) | **POST** /api/accounts/{account_id}/reconcile | Create Reconciliation
*AccountsApi* | [**deleteAccountApiAccountsAccountIdDelete**](docs/AccountsApi.md#deleteaccountapiaccountsaccountiddelete) | **DELETE** /api/accounts/{account_id} | Delete Account
*AccountsApi* | [**deleteAccountApiAccountsAccountIdDelete_0**](docs/AccountsApi.md#deleteaccountapiaccountsaccountiddelete_0) | **DELETE** /api/accounts/{account_id} | Delete Account
*AccountsApi* | [**getAccountApiAccountsAccountIdGet**](docs/AccountsApi.md#getaccountapiaccountsaccountidget) | **GET** /api/accounts/{account_id} | Get Account
*AccountsApi* | [**getAccountApiAccountsAccountIdGet_0**](docs/AccountsApi.md#getaccountapiaccountsaccountidget_0) | **GET** /api/accounts/{account_id} | Get Account
*AccountsApi* | [**getAccountSummaryApiAccountsSummaryGet**](docs/AccountsApi.md#getaccountsummaryapiaccountssummaryget) | **GET** /api/accounts/summary | Get Account Summary
*AccountsApi* | [**getAccountSummaryApiAccountsSummaryGet_0**](docs/AccountsApi.md#getaccountsummaryapiaccountssummaryget_0) | **GET** /api/accounts/summary | Get Account Summary
*AccountsApi* | [**getBalanceHistoryApiAccountsAccountIdBalancesGet**](docs/AccountsApi.md#getbalancehistoryapiaccountsaccountidbalancesget) | **GET** /api/accounts/{account_id}/balances | Get Balance History
*AccountsApi* | [**getBalanceHistoryApiAccountsAccountIdBalancesGet_0**](docs/AccountsApi.md#getbalancehistoryapiaccountsaccountidbalancesget_0) | **GET** /api/accounts/{account_id}/balances | Get Balance History
*AccountsApi* | [**getCalculatedBalanceApiAccountsAccountIdCalculatedBalanceGet**](docs/AccountsApi.md#getcalculatedbalanceapiaccountsaccountidcalculatedbalanceget) | **GET** /api/accounts/{account_id}/calculated-balance | Get Calculated Balance
*AccountsApi* | [**getCalculatedBalanceApiAccountsAccountIdCalculatedBalanceGet_0**](docs/AccountsApi.md#getcalculatedbalanceapiaccountsaccountidcalculatedbalanceget_0) | **GET** /api/accounts/{account_id}/calculated-balance | Get Calculated Balance
*AccountsApi* | [**getCurrentBalanceApiAccountsAccountIdCurrentBalanceGet**](docs/AccountsApi.md#getcurrentbalanceapiaccountsaccountidcurrentbalanceget) | **GET** /api/accounts/{account_id}/current-balance | Get Current Balance
*AccountsApi* | [**getCurrentBalanceApiAccountsAccountIdCurrentBalanceGet_0**](docs/AccountsApi.md#getcurrentbalanceapiaccountsaccountidcurrentbalanceget_0) | **GET** /api/accounts/{account_id}/current-balance | Get Current Balance
*AccountsApi* | [**getHoldingsApiAccountsAccountIdHoldingsGet**](docs/AccountsApi.md#getholdingsapiaccountsaccountidholdingsget) | **GET** /api/accounts/{account_id}/holdings | Get Holdings
*AccountsApi* | [**getHoldingsApiAccountsAccountIdHoldingsGet_0**](docs/AccountsApi.md#getholdingsapiaccountsaccountidholdingsget_0) | **GET** /api/accounts/{account_id}/holdings | Get Holdings
*AccountsApi* | [**getNetWorthApiAccountsNetWorthGet**](docs/AccountsApi.md#getnetworthapiaccountsnetworthget) | **GET** /api/accounts/net-worth | Get Net Worth
*AccountsApi* | [**getNetWorthApiAccountsNetWorthGet_0**](docs/AccountsApi.md#getnetworthapiaccountsnetworthget_0) | **GET** /api/accounts/net-worth | Get Net Worth
*AccountsApi* | [**getPortfolioSummaryApiAccountsAccountIdPortfolioGet**](docs/AccountsApi.md#getportfoliosummaryapiaccountsaccountidportfolioget) | **GET** /api/accounts/{account_id}/portfolio | Get Portfolio Summary
*AccountsApi* | [**getPortfolioSummaryApiAccountsAccountIdPortfolioGet_0**](docs/AccountsApi.md#getportfoliosummaryapiaccountsaccountidportfolioget_0) | **GET** /api/accounts/{account_id}/portfolio | Get Portfolio Summary
*AccountsApi* | [**getReconciliationsApiAccountsAccountIdReconciliationsGet**](docs/AccountsApi.md#getreconciliationsapiaccountsaccountidreconciliationsget) | **GET** /api/accounts/{account_id}/reconciliations | Get Reconciliations
*AccountsApi* | [**getReconciliationsApiAccountsAccountIdReconciliationsGet_0**](docs/AccountsApi.md#getreconciliationsapiaccountsaccountidreconciliationsget_0) | **GET** /api/accounts/{account_id}/reconciliations | Get Reconciliations
*AccountsApi* | [**listAccountsApiAccountsGet**](docs/AccountsApi.md#listaccountsapiaccountsget) | **GET** /api/accounts | List Accounts
*AccountsApi* | [**listAccountsApiAccountsGet_0**](docs/AccountsApi.md#listaccountsapiaccountsget_0) | **GET** /api/accounts | List Accounts
*AccountsApi* | [**updateAccountApiAccountsAccountIdPut**](docs/AccountsApi.md#updateaccountapiaccountsaccountidput) | **PUT** /api/accounts/{account_id} | Update Account
*AccountsApi* | [**updateAccountApiAccountsAccountIdPut_0**](docs/AccountsApi.md#updateaccountapiaccountsaccountidput_0) | **PUT** /api/accounts/{account_id} | Update Account
*AnalysisApi* | [**getCashFlowAnalysisApiAnalysisCashflowGet**](docs/AnalysisApi.md#getcashflowanalysisapianalysiscashflowget) | **GET** /api/analysis/cashflow | Get Cash Flow Analysis
*AnalysisApi* | [**getCashFlowTrendsApiAnalysisCashflowTrendsGet**](docs/AnalysisApi.md#getcashflowtrendsapianalysiscashflowtrendsget) | **GET** /api/analysis/cashflow/trends | Get Cash Flow Trends
*AnalysisApi* | [**getCategoryBreakdownApiAnalysisCategoryBreakdownGet**](docs/AnalysisApi.md#getcategorybreakdownapianalysiscategorybreakdownget) | **GET** /api/analysis/category-breakdown | Get Category Breakdown
*AnalysisApi* | [**getExpenseAnalysisApiAnalysisExpensesGet**](docs/AnalysisApi.md#getexpenseanalysisapianalysisexpensesget) | **GET** /api/analysis/expenses | Get Expense Analysis
*AnalysisApi* | [**getExpenseCategoryTrendsApiAnalysisExpensesCategoryTrendsGet**](docs/AnalysisApi.md#getexpensecategorytrendsapianalysisexpensescategorytrendsget) | **GET** /api/analysis/expenses/category-trends | Get Expense Category Trends
*AnalysisApi* | [**getExpenseTrendsApiAnalysisExpensesTrendsGet**](docs/AnalysisApi.md#getexpensetrendsapianalysisexpensestrendsget) | **GET** /api/analysis/expenses/trends | Get Expense Trends
*AnalysisApi* | [**getFinancialHealthApiAnalysisHealthGet**](docs/AnalysisApi.md#getfinancialhealthapianalysishealthget) | **GET** /api/analysis/health | Get Financial Health
*AnalysisApi* | [**getFinancialSummaryApiAnalysisSummaryGet**](docs/AnalysisApi.md#getfinancialsummaryapianalysissummaryget) | **GET** /api/analysis/summary | Get Financial Summary
*AnalysisApi* | [**getIncomeAnalysisApiAnalysisIncomeGet**](docs/AnalysisApi.md#getincomeanalysisapianalysisincomeget) | **GET** /api/analysis/income | Get Income Analysis
*AnalysisApi* | [**getIncomeExpenseComparisonApiAnalysisIncomeExpenseGet**](docs/AnalysisApi.md#getincomeexpensecomparisonapianalysisincomeexpenseget) | **GET** /api/analysis/income-expense | Get Income Expense Comparison
*AnalysisApi* | [**getIncomeTrendsApiAnalysisIncomeTrendsGet**](docs/AnalysisApi.md#getincometrendsapianalysisincometrendsget) | **GET** /api/analysis/income/trends | Get Income Trends
*CategoriesApi* | [**applyCategoryRulesApiCategoryRulesApplyPost**](docs/CategoriesApi.md#applycategoryrulesapicategoryrulesapplypost) | **POST** /api/category-rules/apply | Apply Category Rules
*CategoriesApi* | [**createCategoryApiCategoriesPost**](docs/CategoriesApi.md#createcategoryapicategoriespost) | **POST** /api/categories | Create Category
*CategoriesApi* | [**createCategoryRuleApiCategoryRulesPost**](docs/CategoriesApi.md#createcategoryruleapicategoryrulespost) | **POST** /api/category-rules | Create Category Rule
*CategoriesApi* | [**deleteCategoryApiCategoriesCategoryIdDelete**](docs/CategoriesApi.md#deletecategoryapicategoriescategoryiddelete) | **DELETE** /api/categories/{category_id} | Delete Category
*CategoriesApi* | [**deleteCategoryRuleApiCategoryRulesRuleIdDelete**](docs/CategoriesApi.md#deletecategoryruleapicategoryrulesruleiddelete) | **DELETE** /api/category-rules/{rule_id} | Delete Category Rule
*CategoriesApi* | [**getCategoryApiCategoriesCategoryIdGet**](docs/CategoriesApi.md#getcategoryapicategoriescategoryidget) | **GET** /api/categories/{category_id} | Get Category
*CategoriesApi* | [**getCategoryRuleApiCategoryRulesRuleIdGet**](docs/CategoriesApi.md#getcategoryruleapicategoryrulesruleidget) | **GET** /api/category-rules/{rule_id} | Get Category Rule
*CategoriesApi* | [**getChildCategoriesApiCategoriesCategoryIdChildrenGet**](docs/CategoriesApi.md#getchildcategoriesapicategoriescategoryidchildrenget) | **GET** /api/categories/{category_id}/children | Get Child Categories
*CategoriesApi* | [**getRootCategoriesApiCategoriesRootGet**](docs/CategoriesApi.md#getrootcategoriesapicategoriesrootget) | **GET** /api/categories/root | Get Root Categories
*CategoriesApi* | [**listCategoriesApiCategoriesGet**](docs/CategoriesApi.md#listcategoriesapicategoriesget) | **GET** /api/categories | List Categories
*CategoriesApi* | [**listCategoryRulesApiCategoryRulesGet**](docs/CategoriesApi.md#listcategoryrulesapicategoryrulesget) | **GET** /api/category-rules | List Category Rules
*CategoriesApi* | [**testCategoryRuleApiCategoryRulesTestPost**](docs/CategoriesApi.md#testcategoryruleapicategoryrulestestpost) | **POST** /api/category-rules/test | Test Category Rule
*CategoriesApi* | [**updateCategoryApiCategoriesCategoryIdPut**](docs/CategoriesApi.md#updatecategoryapicategoriescategoryidput) | **PUT** /api/categories/{category_id} | Update Category
*CategoriesApi* | [**updateCategoryRuleApiCategoryRulesRuleIdPut**](docs/CategoriesApi.md#updatecategoryruleapicategoryrulesruleidput) | **PUT** /api/category-rules/{rule_id} | Update Category Rule
*ClassificationsApi* | [**applyClassificationRulesApiClassificationRulesApplyPost**](docs/ClassificationsApi.md#applyclassificationrulesapiclassificationrulesapplypost) | **POST** /api/classification-rules/apply | Apply Classification Rules
*ClassificationsApi* | [**autoClassifyTransactionsApiTransactionsAutoClassifyPost**](docs/ClassificationsApi.md#autoclassifytransactionsapitransactionsautoclassifypost) | **POST** /api/transactions/auto-classify | Auto-Classify Transactions
*ClassificationsApi* | [**bulkClassifyTransactionsApiTransactionsClassifyBulkPost**](docs/ClassificationsApi.md#bulkclassifytransactionsapitransactionsclassifybulkpost) | **POST** /api/transactions/classify/bulk | Bulk Classify Transactions
*ClassificationsApi* | [**classifyTransactionApiTransactionsTransactionIdClassifyPost**](docs/ClassificationsApi.md#classifytransactionapitransactionstransactionidclassifypost) | **POST** /api/transactions/{transaction_id}/classify | Classify Transaction
*ClassificationsApi* | [**createClassificationApiClassificationsPost**](docs/ClassificationsApi.md#createclassificationapiclassificationspost) | **POST** /api/classifications | Create Classification
*ClassificationsApi* | [**createClassificationRuleApiClassificationRulesPost**](docs/ClassificationsApi.md#createclassificationruleapiclassificationrulespost) | **POST** /api/classification-rules | Create Classification Rule
*ClassificationsApi* | [**deleteClassificationApiClassificationsClassificationIdDelete**](docs/ClassificationsApi.md#deleteclassificationapiclassificationsclassificationiddelete) | **DELETE** /api/classifications/{classification_id} | Delete Classification
*ClassificationsApi* | [**deleteClassificationRuleApiClassificationRulesRuleIdDelete**](docs/ClassificationsApi.md#deleteclassificationruleapiclassificationrulesruleiddelete) | **DELETE** /api/classification-rules/{rule_id} | Delete Classification Rule
*ClassificationsApi* | [**getClassificationApiClassificationsClassificationIdGet**](docs/ClassificationsApi.md#getclassificationapiclassificationsclassificationidget) | **GET** /api/classifications/{classification_id} | Get Classification Details
*ClassificationsApi* | [**getClassificationRuleApiClassificationRulesRuleIdGet**](docs/ClassificationsApi.md#getclassificationruleapiclassificationrulesruleidget) | **GET** /api/classification-rules/{rule_id} | Get Classification Rule
*ClassificationsApi* | [**listClassificationRulesApiClassificationRulesGet**](docs/ClassificationsApi.md#listclassificationrulesapiclassificationrulesget) | **GET** /api/classification-rules | List Classification Rules
*ClassificationsApi* | [**listClassificationsApiClassificationsGet**](docs/ClassificationsApi.md#listclassificationsapiclassificationsget) | **GET** /api/classifications | List All Classifications
*ClassificationsApi* | [**testClassificationRuleApiClassificationRulesTestPost**](docs/ClassificationsApi.md#testclassificationruleapiclassificationrulestestpost) | **POST** /api/classification-rules/test | Test Classification Rule
*ClassificationsApi* | [**updateClassificationApiClassificationsClassificationIdPut**](docs/ClassificationsApi.md#updateclassificationapiclassificationsclassificationidput) | **PUT** /api/classifications/{classification_id} | Update Classification
*ClassificationsApi* | [**updateClassificationRuleApiClassificationRulesRuleIdPut**](docs/ClassificationsApi.md#updateclassificationruleapiclassificationrulesruleidput) | **PUT** /api/classification-rules/{rule_id} | Update Classification Rule
*DefaultApi* | [**healthCheckApiHealthGet**](docs/DefaultApi.md#healthcheckapihealthget) | **GET** /api/health | Health Check
*DefaultApi* | [**rootGet**](docs/DefaultApi.md#rootget) | **GET** / | Root
*ImportApi* | [**getImportDetailApiImportHistoryImportIdGet**](docs/ImportApi.md#getimportdetailapiimporthistoryimportidget) | **GET** /api/import/history/{import_id} | Get Import Detail
*ImportApi* | [**getImportHistoryApiImportHistoryGet**](docs/ImportApi.md#getimporthistoryapiimporthistoryget) | **GET** /api/import/history | Get Import History
*ImportApi* | [**getImportStatusApiImportStatusImportIdGet**](docs/ImportApi.md#getimportstatusapiimportstatusimportidget) | **GET** /api/import/status/{import_id} | Get Import Status
*ImportApi* | [**importFromFilePathApiImportFilePathPost**](docs/ImportApi.md#importfromfilepathapiimportfilepathpost) | **POST** /api/import/file-path | Import From File Path
*ImportApi* | [**importTransactionsApiImportPost**](docs/ImportApi.md#importtransactionsapiimportpost) | **POST** /api/import | Import Transactions
*MaintenanceApi* | [**fixClassificationsApiMaintenanceFixClassificationsPost**](docs/MaintenanceApi.md#fixclassificationsapimaintenancefixclassificationspost) | **POST** /api/maintenance/fix/classifications | Fix System Classifications
*MaintenanceApi* | [**fixClassificationsApiMaintenanceFixClassificationsPost_0**](docs/MaintenanceApi.md#fixclassificationsapimaintenancefixclassificationspost_0) | **POST** /api/maintenance/fix/classifications | Fix System Classifications
*MaintenanceApi* | [**fixReimbursementsApiMaintenanceFixReimbursementsPost**](docs/MaintenanceApi.md#fixreimbursementsapimaintenancefixreimbursementspost) | **POST** /api/maintenance/fix/reimbursements | Fix Reimbursement Links
*MaintenanceApi* | [**fixReimbursementsApiMaintenanceFixReimbursementsPost_0**](docs/MaintenanceApi.md#fixreimbursementsapimaintenancefixreimbursementspost_0) | **POST** /api/maintenance/fix/reimbursements | Fix Reimbursement Links
*MaintenanceApi* | [**fixTransfersApiMaintenanceFixTransfersPost**](docs/MaintenanceApi.md#fixtransfersapimaintenancefixtransferspost) | **POST** /api/maintenance/fix/transfers | Fix Transfer Links
*MaintenanceApi* | [**fixTransfersApiMaintenanceFixTransfersPost_0**](docs/MaintenanceApi.md#fixtransfersapimaintenancefixtransferspost_0) | **POST** /api/maintenance/fix/transfers | Fix Transfer Links
*PersonsApi* | [**createPersonApiPersonsPost**](docs/PersonsApi.md#createpersonapipersonspost) | **POST** /api/persons/ | Create Person
*PersonsApi* | [**createPersonApiPersonsPost_0**](docs/PersonsApi.md#createpersonapipersonspost_0) | **POST** /api/persons/ | Create Person
*PersonsApi* | [**listPersonsApiPersonsGet**](docs/PersonsApi.md#listpersonsapipersonsget) | **GET** /api/persons/ | List Persons
*PersonsApi* | [**listPersonsApiPersonsGet_0**](docs/PersonsApi.md#listpersonsapipersonsget_0) | **GET** /api/persons/ | List Persons
*ProjectionsApi* | [**getScenariosApiProjectionsScenariosGet**](docs/ProjectionsApi.md#getscenariosapiprojectionsscenariosget) | **GET** /api/projections/scenarios | Get Scenario Analysis
*ProjectionsApi* | [**projectCashflowApiProjectionsCashflowGet**](docs/ProjectionsApi.md#projectcashflowapiprojectionscashflowget) | **GET** /api/projections/cashflow | Project Future Cash Flow
*ProjectionsApi* | [**projectExpensesApiProjectionsExpensesGet**](docs/ProjectionsApi.md#projectexpensesapiprojectionsexpensesget) | **GET** /api/projections/expenses | Project Future Expenses
*ProjectionsApi* | [**projectIncomeApiProjectionsIncomeGet**](docs/ProjectionsApi.md#projectincomeapiprojectionsincomeget) | **GET** /api/projections/income | Project Future Income
*ProjectionsApi* | [**validateProjectionApiProjectionsValidatePost**](docs/ProjectionsApi.md#validateprojectionapiprojectionsvalidatepost) | **POST** /api/projections/validate | Validate Projection Accuracy
*RelationshipsApi* | [**createRelationshipApiRelationshipsPost**](docs/RelationshipsApi.md#createrelationshipapirelationshipspost) | **POST** /api/relationships | Create Relationship
*RelationshipsApi* | [**deleteRelationshipApiRelationshipsRelationshipIdDelete**](docs/RelationshipsApi.md#deleterelationshipapirelationshipsrelationshipiddelete) | **DELETE** /api/relationships/{relationship_id} | Delete Relationship
*RelationshipsApi* | [**detectAllRelationshipsApiRelationshipsDetectAllPost**](docs/RelationshipsApi.md#detectallrelationshipsapirelationshipsdetectallpost) | **POST** /api/relationships/detect/all | Detect All Relationships
*RelationshipsApi* | [**detectCreditCardPairsApiRelationshipsDetectCreditCardsPost**](docs/RelationshipsApi.md#detectcreditcardpairsapirelationshipsdetectcreditcardspost) | **POST** /api/relationships/detect/credit-cards | Detect Credit Card Pairs
*RelationshipsApi* | [**detectDividendReinvestmentPairsApiRelationshipsDetectDividendReinvestmentsPost**](docs/RelationshipsApi.md#detectdividendreinvestmentpairsapirelationshipsdetectdividendreinvestmentspost) | **POST** /api/relationships/detect/dividend-reinvestments | Detect Dividend Reinvestment Pairs
*RelationshipsApi* | [**detectReimbursementPairsApiRelationshipsDetectReimbursementsPost**](docs/RelationshipsApi.md#detectreimbursementpairsapirelationshipsdetectreimbursementspost) | **POST** /api/relationships/detect/reimbursements | Detect Reimbursement Pairs
*RelationshipsApi* | [**detectTransferPairsApiRelationshipsDetectTransfersPost**](docs/RelationshipsApi.md#detecttransferpairsapirelationshipsdetecttransferspost) | **POST** /api/relationships/detect/transfers | Detect Transfer Pairs
*RelationshipsApi* | [**getRelatedTransactionsApiTransactionsTransactionIdRelationshipsGet**](docs/RelationshipsApi.md#getrelatedtransactionsapitransactionstransactionidrelationshipsget) | **GET** /api/transactions/{transaction_id}/relationships | Get Related Transactions
*ReportsApi* | [**getBalanceReportApiReportsBalancesGet**](docs/ReportsApi.md#getbalancereportapireportsbalancesget) | **GET** /api/reports/balances | Generate Balance Sheet / Net Worth Report
*ReportsApi* | [**getExpenseDetailReportApiReportsExpensesGet**](docs/ReportsApi.md#getexpensedetailreportapireportsexpensesget) | **GET** /api/reports/expenses | Generate Expense Detail Report
*ReportsApi* | [**getIncomeDetailReportApiReportsIncomeGet**](docs/ReportsApi.md#getincomedetailreportapireportsincomeget) | **GET** /api/reports/income | Generate Income Detail Report
*ReportsApi* | [**getReconciliationReportApiReportsReconciliationGet**](docs/ReportsApi.md#getreconciliationreportapireportsreconciliationget) | **GET** /api/reports/reconciliation | Generate Reconciliation Report
*ReportsApi* | [**getSummaryReportApiReportsSummaryGet**](docs/ReportsApi.md#getsummaryreportapireportssummaryget) | **GET** /api/reports/summary | Generate Summary Report
*ScenariosApi* | [**previewScenarioApiScenariosPreviewPost**](docs/ScenariosApi.md#previewscenarioapiscenariospreviewpost) | **POST** /api/scenarios/preview | Preview Scenario
*ScenariosApi* | [**previewScenarioApiScenariosPreviewPost_0**](docs/ScenariosApi.md#previewscenarioapiscenariospreviewpost_0) | **POST** /api/scenarios/preview | Preview Scenario
*SplitsApi* | [**createTransactionSplitApiTransactionsTransactionIdSplitsPost**](docs/SplitsApi.md#createtransactionsplitapitransactionstransactionidsplitspost) | **POST** /api/transactions/{transaction_id}/splits | Create Transaction Split
*SplitsApi* | [**createTransactionSplitApiTransactionsTransactionIdSplitsPost_0**](docs/SplitsApi.md#createtransactionsplitapitransactionstransactionidsplitspost_0) | **POST** /api/transactions/{transaction_id}/splits | Create Transaction Split
*SplitsApi* | [**getTransactionSplitsApiTransactionsTransactionIdSplitsGet**](docs/SplitsApi.md#gettransactionsplitsapitransactionstransactionidsplitsget) | **GET** /api/transactions/{transaction_id}/splits | Get Transaction Splits
*SplitsApi* | [**getTransactionSplitsApiTransactionsTransactionIdSplitsGet_0**](docs/SplitsApi.md#gettransactionsplitsapitransactionstransactionidsplitsget_0) | **GET** /api/transactions/{transaction_id}/splits | Get Transaction Splits
*TransactionsApi* | [**createTransactionApiTransactionsPost**](docs/TransactionsApi.md#createtransactionapitransactionspost) | **POST** /api/transactions | Create Transaction
*TransactionsApi* | [**deleteTransactionApiTransactionsTransactionIdDelete**](docs/TransactionsApi.md#deletetransactionapitransactionstransactioniddelete) | **DELETE** /api/transactions/{transaction_id} | Delete Transaction
*TransactionsApi* | [**getTransactionApiTransactionsTransactionIdGet**](docs/TransactionsApi.md#gettransactionapitransactionstransactionidget) | **GET** /api/transactions/{transaction_id} | Get Transaction
*TransactionsApi* | [**listTransactionsApiTransactionsGet**](docs/TransactionsApi.md#listtransactionsapitransactionsget) | **GET** /api/transactions | List Transactions
*TransactionsApi* | [**updateTransactionApiTransactionsTransactionIdPut**](docs/TransactionsApi.md#updatetransactionapitransactionstransactionidput) | **PUT** /api/transactions/{transaction_id} | Update Transaction


### Models

- [AccountBalanceDetail](docs/AccountBalanceDetail.md)
- [AccountCreate](docs/AccountCreate.md)
- [AccountResponse](docs/AccountResponse.md)
- [AccountSummary](docs/AccountSummary.md)
- [AccountUpdate](docs/AccountUpdate.md)
- [AccuracyMetrics](docs/AccuracyMetrics.md)
- [Amount](docs/Amount.md)
- [Amount1](docs/Amount1.md)
- [Amount2](docs/Amount2.md)
- [AnalysisModeEnumOutput](docs/AnalysisModeEnumOutput.md)
- [ApplyCategoryRulesRequest](docs/ApplyCategoryRulesRequest.md)
- [ApplyCategoryRulesResponse](docs/ApplyCategoryRulesResponse.md)
- [ApplyRulesRequest](docs/ApplyRulesRequest.md)
- [ApplyRulesResponse](docs/ApplyRulesResponse.md)
- [AutoClassifyRequest](docs/AutoClassifyRequest.md)
- [AutoClassifyResponse](docs/AutoClassifyResponse.md)
- [BalanceCreate](docs/BalanceCreate.md)
- [BalanceHistory](docs/BalanceHistory.md)
- [BalanceReportResponse](docs/BalanceReportResponse.md)
- [BalanceResponse](docs/BalanceResponse.md)
- [BalanceSummary](docs/BalanceSummary.md)
- [BulkClassifyRequest](docs/BulkClassifyRequest.md)
- [BulkClassifyResponse](docs/BulkClassifyResponse.md)
- [CalculatedBalance](docs/CalculatedBalance.md)
- [CashBalance](docs/CashBalance.md)
- [CashFlowResponse](docs/CashFlowResponse.md)
- [CashFlowTrendPoint](docs/CashFlowTrendPoint.md)
- [CashFlowTrendsResponse](docs/CashFlowTrendsResponse.md)
- [CashflowDailyProjection](docs/CashflowDailyProjection.md)
- [CashflowProjectionResponse](docs/CashflowProjectionResponse.md)
- [CashflowSummary](docs/CashflowSummary.md)
- [CategoryBreakdown](docs/CategoryBreakdown.md)
- [CategoryBreakdownItem](docs/CategoryBreakdownItem.md)
- [CategoryBreakdownResponse](docs/CategoryBreakdownResponse.md)
- [CategoryCreate](docs/CategoryCreate.md)
- [CategoryDetail](docs/CategoryDetail.md)
- [CategoryInfo](docs/CategoryInfo.md)
- [CategoryListResponse](docs/CategoryListResponse.md)
- [CategoryResponse](docs/CategoryResponse.md)
- [CategoryRuleCreate](docs/CategoryRuleCreate.md)
- [CategoryRuleListResponse](docs/CategoryRuleListResponse.md)
- [CategoryRuleResponse](docs/CategoryRuleResponse.md)
- [CategoryRuleUpdate](docs/CategoryRuleUpdate.md)
- [CategorySummary](docs/CategorySummary.md)
- [CategoryUpdate](docs/CategoryUpdate.md)
- [ClassificationCreate](docs/ClassificationCreate.md)
- [ClassificationInfo](docs/ClassificationInfo.md)
- [ClassificationListResponse](docs/ClassificationListResponse.md)
- [ClassificationResponse](docs/ClassificationResponse.md)
- [ClassificationRuleCreate](docs/ClassificationRuleCreate.md)
- [ClassificationRuleListResponse](docs/ClassificationRuleListResponse.md)
- [ClassificationRuleResponse](docs/ClassificationRuleResponse.md)
- [ClassificationRuleUpdate](docs/ClassificationRuleUpdate.md)
- [ClassificationUpdate](docs/ClassificationUpdate.md)
- [ClassifyTransactionRequest](docs/ClassifyTransactionRequest.md)
- [ConfidenceInterval](docs/ConfidenceInterval.md)
- [CostBasis](docs/CostBasis.md)
- [CreditCardPairDetection](docs/CreditCardPairDetection.md)
- [CreditCardPairsResponse](docs/CreditCardPairsResponse.md)
- [CurrentValue](docs/CurrentValue.md)
- [DailyProjection](docs/DailyProjection.md)
- [DetectAllRelationshipsResponse](docs/DetectAllRelationshipsResponse.md)
- [DividendReinvestmentPairDetection](docs/DividendReinvestmentPairDetection.md)
- [DividendReinvestmentPairsResponse](docs/DividendReinvestmentPairsResponse.md)
- [ExpenseAnalysisResponse](docs/ExpenseAnalysisResponse.md)
- [ExpenseDetailReportResponse](docs/ExpenseDetailReportResponse.md)
- [ExpenseProjectionResponse](docs/ExpenseProjectionResponse.md)
- [ExpenseSummary](docs/ExpenseSummary.md)
- [FinancialHealthResponse](docs/FinancialHealthResponse.md)
- [FinancialSummaryResponse](docs/FinancialSummaryResponse.md)
- [FixResult](docs/FixResult.md)
- [HTTPValidationError](docs/HTTPValidationError.md)
- [HealthIndicators](docs/HealthIndicators.md)
- [HistoricalPeriod](docs/HistoricalPeriod.md)
- [HoldingCreate](docs/HoldingCreate.md)
- [HoldingResponse](docs/HoldingResponse.md)
- [ImportErrorDetail](docs/ImportErrorDetail.md)
- [ImportHistoryDetailResponse](docs/ImportHistoryDetailResponse.md)
- [ImportHistoryItem](docs/ImportHistoryItem.md)
- [ImportHistoryResponse](docs/ImportHistoryResponse.md)
- [ImportRequest](docs/ImportRequest.md)
- [ImportResponse](docs/ImportResponse.md)
- [ImportStatusResponse](docs/ImportStatusResponse.md)
- [IncomeAnalysisResponse](docs/IncomeAnalysisResponse.md)
- [IncomeDetailReportResponse](docs/IncomeDetailReportResponse.md)
- [IncomeExpenseComparisonResponse](docs/IncomeExpenseComparisonResponse.md)
- [IncomeProjectionResponse](docs/IncomeProjectionResponse.md)
- [IncomeSummary](docs/IncomeSummary.md)
- [InvestmentValue](docs/InvestmentValue.md)
- [MaxAmount](docs/MaxAmount.md)
- [MinAmount](docs/MinAmount.md)
- [ModelMetrics](docs/ModelMetrics.md)
- [NetWorthResponse](docs/NetWorthResponse.md)
- [OpeningBalance](docs/OpeningBalance.md)
- [PersonCreate](docs/PersonCreate.md)
- [PersonRead](docs/PersonRead.md)
- [PortfolioSummary](docs/PortfolioSummary.md)
- [ProjectionMethodEnum](docs/ProjectionMethodEnum.md)
- [ProjectionPeriod](docs/ProjectionPeriod.md)
- [Quantity](docs/Quantity.md)
- [RecentTransaction](docs/RecentTransaction.md)
- [ReconciliationComplete](docs/ReconciliationComplete.md)
- [ReconciliationCreate](docs/ReconciliationCreate.md)
- [ReconciliationReportResponse](docs/ReconciliationReportResponse.md)
- [ReconciliationResponse](docs/ReconciliationResponse.md)
- [ReconciliationSummary](docs/ReconciliationSummary.md)
- [ReimbursementPairDetection](docs/ReimbursementPairDetection.md)
- [ReimbursementPairsResponse](docs/ReimbursementPairsResponse.md)
- [RelatedTransactionInfo](docs/RelatedTransactionInfo.md)
- [RelatedTransactionsResponse](docs/RelatedTransactionsResponse.md)
- [RelationshipCreateRequest](docs/RelationshipCreateRequest.md)
- [RelationshipResponse](docs/RelationshipResponse.md)
- [ReportFormatEnum](docs/ReportFormatEnum.md)
- [ReportPeriod](docs/ReportPeriod.md)
- [ScenarioAdjusterIn](docs/ScenarioAdjusterIn.md)
- [ScenarioData](docs/ScenarioData.md)
- [ScenarioKPIs](docs/ScenarioKPIs.md)
- [ScenarioPreviewRequest](docs/ScenarioPreviewRequest.md)
- [ScenarioPreviewResponse](docs/ScenarioPreviewResponse.md)
- [ScenarioRange](docs/ScenarioRange.md)
- [Scenarios](docs/Scenarios.md)
- [SeriesPoint](docs/SeriesPoint.md)
- [SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum](docs/SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum.md)
- [SrcFinancialAnalysisApiSchemasReportAnalysisModeEnum](docs/SrcFinancialAnalysisApiSchemasReportAnalysisModeEnum.md)
- [StartingBalance](docs/StartingBalance.md)
- [StatementBalance](docs/StatementBalance.md)
- [StatementCashBalance](docs/StatementCashBalance.md)
- [StatementInvestmentValue](docs/StatementInvestmentValue.md)
- [SuccessResponse](docs/SuccessResponse.md)
- [SummaryReportResponse](docs/SummaryReportResponse.md)
- [TagInfo](docs/TagInfo.md)
- [TestCategoryRuleRequest](docs/TestCategoryRuleRequest.md)
- [TestCategoryRuleResponse](docs/TestCategoryRuleResponse.md)
- [TestRuleRequest](docs/TestRuleRequest.md)
- [TestRuleResponse](docs/TestRuleResponse.md)
- [TimePeriodEnum](docs/TimePeriodEnum.md)
- [TopCategory](docs/TopCategory.md)
- [TotalBalance](docs/TotalBalance.md)
- [TransactionClearRequest](docs/TransactionClearRequest.md)
- [TransactionCreate](docs/TransactionCreate.md)
- [TransactionDetail](docs/TransactionDetail.md)
- [TransactionListResponse](docs/TransactionListResponse.md)
- [TransactionResponse](docs/TransactionResponse.md)
- [TransactionSplitCreate](docs/TransactionSplitCreate.md)
- [TransactionSplitRead](docs/TransactionSplitRead.md)
- [TransactionSummary](docs/TransactionSummary.md)
- [TransactionUpdate](docs/TransactionUpdate.md)
- [TransferPairDetection](docs/TransferPairDetection.md)
- [TransferPairsResponse](docs/TransferPairsResponse.md)
- [TrendDataPoint](docs/TrendDataPoint.md)
- [TrendsResponse](docs/TrendsResponse.md)
- [ValidationError](docs/ValidationError.md)
- [ValidationErrorLocInner](docs/ValidationErrorLocInner.md)
- [ValidationRequest](docs/ValidationRequest.md)

### Authorization


Authentication schemes defined for the API:
<a id="bearerAuth"></a>
#### bearerAuth


- **Type**: HTTP Bearer Token authentication (JWT)
<a id="apiKey"></a>
#### apiKey


- **Type**: API key
- **API key parameter name**: `X-API-Key`
- **Location**: HTTP header

## About

This TypeScript SDK client supports the [Fetch API](https://fetch.spec.whatwg.org/)
and is automatically generated by the
[OpenAPI Generator](https://openapi-generator.tech) project:

- API version: `1.0.0`
- Package version: `0.1.0`
- Generator version: `7.18.0-SNAPSHOT`
- Build package: `org.openapitools.codegen.languages.TypeScriptFetchClientCodegen`

The generated npm module supports the following:

- Environments
  * Node.js
  * Webpack
  * Browserify
- Language levels
  * ES5 - you must have a Promises/A+ library installed
  * ES6
- Module systems
  * CommonJS
  * ES6 module system


## Development

### Building

To build the TypeScript source code, you need to have Node.js and npm installed.
After cloning the repository, navigate to the project directory and run:

```bash
npm install
npm run build
```

### Publishing

Once you've built the package, you can publish it to npm:

```bash
npm publish
```

## License

[]()
