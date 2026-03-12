# Demo Prompts for Postman MCP

## Prompt 1: Create Test Collection

```
using the postman mcp, create a standalone test collection for the reports routes in 
core-api/src/financial_analysis/api/routes/reports.py

make it its own collection, not a folder in an existing collection. 
add comprehensive test scripts to each endpoint.
the workspace id is in dev-tools/.env
```

## Prompt 2: Add Mock Server

```
add a mock server to that collection with example responses for all endpoints
```

---

## What These Prompts Do

**Prompt 1** creates:
- Standalone collection (not a folder)
- All endpoints from the reports.py file
- Test scripts for each endpoint
- Local development environment
- Configuration saved to .postman.json

**Prompt 2** creates:
- Mock server for the collection
- Example responses for all 6 endpoints
- Mock server environment
- Updates .postman.json with mock details

## Expected Results

After Prompt 1:
- Collection: "Spearmint Reports API Tests" with 6 endpoints
- Environment: "Spearmint - Local Development" (http://localhost:8000)
- File: .postman.json with all IDs

After Prompt 2:
- Mock server with public URL
- Environment: "Spearmint - Mock Server" 
- All endpoints return realistic mock data
- Updated .postman.json
