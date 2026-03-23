import { SpearmintApi } from "@spearmint-finance/sdk";

// SDK Base URL Configuration (3-tier priority):
// 1. VITE_API_URL environment variable (if set)
// 2. window.location.origin (browser's current URL)
// 3. Fallback: http://localhost:8080 (API Gateway)
//
// The SDK appends /api/* to the baseUrl for all requests.
//
// Local Development (Vite proxy - RECOMMENDED):
//   - VITE_API_URL unset → uses window.location.origin (http://localhost:5173)
//   - SDK calls: http://localhost:5173/api/transactions
//   - Vite proxy forwards to: http://localhost:8000/api/transactions
//   - Flow: SDK → Vite Proxy → Core API
//
// Local Development (Direct API - ALTERNATIVE):
//   - VITE_API_URL=http://localhost:8000/api
//   - SDK calls: http://localhost:8000/api/transactions
//   - Flow: SDK → Core API (bypasses proxy)
//
// Docker Development (API Gateway):
//   - VITE_API_URL=http://localhost:8080
//   - SDK calls: http://localhost:8080/api/transactions
//   - Flow: SDK → API Gateway → Core API
//
// Production:
//   - VITE_API_URL unset → uses window.location.origin (https://example.com)
//   - SDK calls: https://example.com/api/transactions
//   - Flow: SDK → API Gateway → Core API
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
export const maintenanceApi = sdk.maintenance;
export const analysisApi = sdk.analysis;
export const projectionsApi = sdk.projections;
export const scenariosApi = sdk.scenarios;
export const importApi = sdk.import_;
export const categoriesApi = sdk.categories;
export const relationshipsApi = sdk.relationships;
export const personsApi = sdk.persons;
export const splitsApi = sdk.splits;
export const entitiesApi = sdk.entities;

// Also export the main SDK instance for direct access
export default sdk;
