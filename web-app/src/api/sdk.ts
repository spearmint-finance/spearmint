import { SpearmintApi } from "@spearmint-finance/sdk";

// The SDK already includes /api in all paths, so baseUrl should be the root origin
// For Docker: use window.location.origin (e.g., http://localhost:8080)
// For dev with Vite proxy: use window.location.origin (e.g., http://localhost:5173)
// The SDK will append /api/* to this base URL
const baseUrl =
  import.meta.env.VITE_API_URL ||
  (typeof window !== "undefined"
    ? window.location.origin
    : "http://localhost:8080");

// Initialize the SDK with configuration
const sdk = new SpearmintApi({
  baseUrl: baseUrl,
  // Add token here if authentication is needed
  // token: 'YOUR_TOKEN',
});

// Export individual service instances for backward compatibility
export const systemApi = sdk.system;
export const transactionsApi = sdk.transactions;
export const accountsApi = sdk.accounts;
export const reportsApi = sdk.reports;
export const classificationsApi = sdk.classifications;
export const maintenanceApi = sdk.maintenance;
export const analysisApi = sdk.analysis;
export const projectionsApi = sdk.projections;
export const scenariosApi = sdk.scenarios;
export const importApi = sdk.import_;
export const categoriesApi = sdk.categories;
export const relationshipsApi = sdk.relationships;
export const personsApi = sdk.persons;
export const splitsApi = sdk.splits;

// Also export the main SDK instance for direct access
export default sdk;
