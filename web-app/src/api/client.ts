import axios from "axios";

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000/api",
  timeout: 30000,
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    // Log POST requests for debugging
    if (config.method === "post" && config.url?.includes("/transactions")) {
      console.log("=== POST Request ===");
      console.log("URL:", config.url);
      console.log("Data:", config.data);
    }

    // Add auth token if available (for future authentication)
    const token = localStorage.getItem("authToken");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Handle common errors
    if (error.response) {
      // Server responded with error status
      const { status, data } = error.response;

      // Log full error response for debugging
      console.error("=== API Error Response ===");
      console.error("Status:", status);
      console.error("Data:", data);

      switch (status) {
        case 401:
          // Unauthorized - clear auth and redirect to login
          localStorage.removeItem("authToken");
          // Future: redirect to login page
          break;
        case 403:
          // Forbidden
          console.error("Access forbidden:", data.message || data.detail);
          break;
        case 404:
          // Not found
          console.error("Resource not found:", data.message || data.detail);
          break;
        case 500:
          // Server error
          console.error("Server error:", data.message || data.detail);
          break;
        default:
          console.error(
            "API error:",
            data.message || data.detail || JSON.stringify(data)
          );
      }
    } else if (error.request) {
      // Request made but no response received
      console.error("Network error: No response from server");
    } else {
      // Error in request setup
      console.error("Request error:", error.message);
    }

    return Promise.reject(error);
  }
);

export default apiClient;
