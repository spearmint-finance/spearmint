import { 
    Configuration, 
    TransactionsApi, 
    AccountsApi, 
    ReportsApi, 
    ClassificationsApi,
    MaintenanceApi,
    AnalysisApi,
    ProjectionsApi,
    ScenariosApi,
    ImportApi,
    CategoriesApi,
    RelationshipsApi,
    PersonsApi,
    SplitsApi
} from "@spearmint-money/sdk";

const basePath = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

const config = new Configuration({
    basePath: basePath,
    // Add middleware/interceptors here if the SDK supports it (middleware in openapi-generator fetch)
    // or generated fetchApi implementation.
});

export const transactionsApi = new TransactionsApi(config);
export const accountsApi = new AccountsApi(config);
export const reportsApi = new ReportsApi(config);
export const classificationsApi = new ClassificationsApi(config);
export const maintenanceApi = new MaintenanceApi(config);
export const analysisApi = new AnalysisApi(config);
export const projectionsApi = new ProjectionsApi(config);
export const scenariosApi = new ScenariosApi(config);
export const importApi = new ImportApi(config);
export const categoriesApi = new CategoriesApi(config);
export const relationshipsApi = new RelationshipsApi(config);
export const personsApi = new PersonsApi(config);
export const splitsApi = new SplitsApi(config);
