# Postman Collection Extractor

A reusable tool for extracting and analyzing any Postman collection by its ID. Generates API overview reports and detailed endpoint listings.

## Overview

This tool suite fetches Postman collections via the Postman API and automatically parses them to produce:
- **Collection JSON**: Raw collection data for programmatic use
- **Overview Report** (`.txt`): Human-readable summary of all endpoints grouped by API section
- **Endpoint CSV** (`.csv`): Structured data for import into spreadsheets or databases

## Prerequisites

- **PowerShell 5.1+** (Windows) or PowerShell Core (cross-platform)
- **Python 3.7+** with standard library (no external dependencies)
- **Postman API Key**: Get from https://web.postman.co/settings/me/api-keys
- **Collection ID**: Available from the collection's public link

## Setup

### 1. Get Your Postman API Key

1. Go to https://web.postman.co/settings/me/api-keys
2. Click "Generate API Key"
3. Copy the key to your clipboard

### 2. Set Environment Variable (Recommended)

Store your API key as an environment variable to avoid passing it on the command line:

**PowerShell (Temporary - Current Session)**:
```powershell
$env:POSTMAN_API_KEY = "your_api_key_here"
```

**PowerShell (Permanent - All Sessions)**:
```powershell
[Environment]::SetEnvironmentVariable("POSTMAN_API_KEY", "your_api_key_here", "User")
```

**Windows Command Prompt**:
```cmd
setx POSTMAN_API_KEY "your_api_key_here"
```

### 3. Find Your Collection ID

For public collections, the ID is in the URL:
- Link: `https://www.postman.com/{workspace}/{collection_name}/overview`
- Collection ID: The UUID in the collection menu → "Share" → "Via URL" or browser address bar

Example collection ID: `19931619-c8ba23fd-94d7-4737-8ca6-1743b4952531`

## Usage

### Basic Usage

```powershell
.\extract_collection.ps1 -CollectionId "19931619-c8ba23fd-94d7-4737-8ca6-1743b4952531"
```

Outputs to current directory:
- `{collection_name}_collection.json`
- `{collection_name}_overview.txt`
- `{collection_name}_endpoints.csv`

### Advanced Usage

```powershell
# Specify output directory
.\extract_collection.ps1 `
  -CollectionId "19931619-c8ba23fd-94d7-4737-8ca6-1743b4952531" `
  -OutputDir "C:\Reports"

# Skip report generation (JSON only)
.\extract_collection.ps1 `
  -CollectionId "19931619-c8ba23fd-94d7-4737-8ca6-1743b4952531" `
  -SkipReport

# Pass API key directly (not recommended)
.\extract_collection.ps1 `
  -CollectionId "19931619-c8ba23fd-94d7-4737-8ca6-1743b4952531" `
  -ApiKey "your_api_key_here"
```

### Parameters

| Parameter | Required | Type | Default | Description |
|-----------|----------|------|---------|-------------|
| `CollectionId` | Yes | String | — | Postman collection UUID |
| `ApiKey` | No | String | `$env:POSTMAN_API_KEY` | Postman API key (use env var if not specified) |
| `OutputDir` | No | String | Current directory | Directory to save output files |
| `SkipReport` | No | Switch | `$false` | If set, skips Python analysis and CSV generation |

## Output Format

### Overview Report (`*_overview.txt`)

Human-readable summary with endpoint counts and groupings:

```
========================================
POSTMAN COLLECTION OVERVIEW
========================================

Collection: Guide REST API
Total Endpoints: 70

ENDPOINTS BY RESOURCE:
────────────────────────────────────────

[Badge Management] 8 endpoints

  GET    /badges/{id}
  GET    /api/v2/badges
  POST   /api/v2/badges
  ...

[Content Tags] 6 endpoints

  DELETE /api/v2/content_tags/{id}
  GET    /api/v2/content_tags
  ...

METHOD DISTRIBUTION:
────────────────────────────────────────
GET    : 23
POST   : 20
DELETE : 19
PUT    : 7
PATCH  : 1
TOTAL  : 70
```

### Endpoint CSV (`*_endpoints.csv`)

Structured data for analysis:

```csv
Section,Endpoint Name,HTTP Method,URL Path
Badge Management,Get All Badges,GET,/api/v2/badges
Badge Management,Create Badges,POST,/api/v2/badges
Badge Management,Get Badge by ID,GET,/badges/{id}
Content Tags,List Content Tags,GET,/api/v2/content_tags
...
```

### Collection JSON (`*_collection.json`)

Raw Postman collection in standard format. Useful for:
- Importing into Postman desktop app
- Programmatic analysis
- Integration with other tools

## Examples

### Extract the Guide REST API Collection

```powershell
$env:POSTMAN_API_KEY = "your_key_here"
.\extract_collection.ps1 -CollectionId "19931619-c8ba23fd-94d7-4737-8ca6-1743b4952531"
```

**Output**:
- `guide_rest_api_collection.json` (2.2 MB)
- `guide_rest_api_overview.txt` (formatted report)
- `guide_rest_api_endpoints.csv` (all 70 endpoints)

### Compare Two API Collections

```powershell
# Extract first API
.\extract_collection.ps1 -CollectionId "id-of-api-v1" -OutputDir ".\reports\v1"

# Extract second API
.\extract_collection.ps1 -CollectionId "id-of-api-v2" -OutputDir ".\reports\v2"

# Use your preferred diff tool
diff .\reports\v1\*_overview.txt .\reports\v2\*_overview.txt
```

### Automated Reporting

```powershell
# Extract multiple collections into a single report directory
$collections = @(
    "id-collection-1",
    "id-collection-2",
    "id-collection-3"
)

foreach ($id in $collections) {
    .\extract_collection.ps1 -CollectionId $id -OutputDir ".\all_reports"
    Write-Host "Extracted collection: $id"
}
```

## Troubleshooting

### Error: "Postman API key not found"

**Cause**: POSTMAN_API_KEY environment variable not set or empty

**Solution**:
```powershell
$env:POSTMAN_API_KEY = "your_api_key_here"
# Or pass with -ApiKey parameter
.\extract_collection.ps1 -CollectionId "..." -ApiKey "your_api_key_here"
```

### Error: "401 Unauthorized" from Postman API

**Cause**: Invalid or expired API key

**Solution**: 
1. Regenerate your API key at https://web.postman.co/settings/me/api-keys
2. Update your environment variable
3. Try again

### Error: "404 Not Found" from Postman API

**Cause**: Invalid collection ID or collection does not exist

**Solution**:
1. Verify the collection ID is correct
2. Ensure the collection is shared publicly (if using a private collection, use a full access token)
3. Check the collection still exists

### Error: "Python: No module named 'json'"

**Cause**: Python installation corrupted or path issue

**Solution**:
```powershell
# Verify Python installation
python --version

# Manually run the analyzer
python analyze_collection.py "path\to\collection.json" "output_dir"
```

### JSON File Not Created

**Cause**: Output directory doesn't exist or permission denied

**Solution**:
```powershell
# Ensure output directory exists
if (-not (Test-Path ".\my_output")) {
    New-Item -ItemType Directory -Path ".\my_output"
}
.\extract_collection.ps1 -CollectionId "..." -OutputDir ".\my_output"
```

## Architecture

### extract_collection.ps1

**Role**: Orchestrator script
- Fetches collection from Postman API using provided collection ID
- Validates API key and parameters
- Saves raw JSON to disk
- Invokes Python analyzer for report generation

**Dependencies**: None (uses only built-in PowerShell cmdlets)

### analyze_collection.py

**Role**: JSON parser and report generator
- Reads Postman collection JSON
- Recursively extracts endpoints from nested folder structure
- Groups endpoints by top-level resource category
- Generates formatted text overview
- Exports structured CSV for spreadsheet import

**Dependencies**: Standard library only (json, sys, argparse, pathlib, defaultdict, csv)

## File Structure

```
collection_extractor/
├── README.md                    # This file
├── extract_collection.ps1       # PowerShell orchestrator
└── analyze_collection.py        # Python analyzer
```

## API Reference

### Postman API Endpoint

```
GET https://api.getpostman.com/collections/{collectionId}
Header: X-Api-Key: {API_KEY}
```

Returns complete collection definition in JSON format (Postman v2.0 schema).

## Limitations

- **Public collections only** (via standard API key)
- For private collections, use a Postman full-access token instead
- Large collections (>50 MB) may require increased system memory
- URL paths are extracted as-is from collection; variables are not resolved

## Performance Notes

- Typical collection (50-100 endpoints): <2 seconds total
- Large collection (500+ endpoints): 5-10 seconds
- Network latency dominates; local processing is negligible

## License

Part of the Spearmint project. Use according to project license terms.

## Support

For issues or feature requests, refer to the main Spearmint project documentation.
