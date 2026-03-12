# Notion Work History Tracker Setup

## Quick Start

### 1. Create Notion Integration

1. Go to https://www.notion.so/my-integrations
2. Click **"+ New integration"**
3. Give it a name (e.g., "Work History Tracker")
4. Select your workspace
5. Copy the **Internal Integration Token** (starts with `secret_`)

### 2. Create Notion Database

1. In Notion, create a new page
2. Add a **Database - Full page**
3. Name it "Work History" (or whatever you prefer)
4. Add these properties:
   - **Title** (title) - Already exists
   - **Date** (date) - Click "+" → Date
   - **Description** (rich_text) - Click "+" → Text
   - **Duration** (number) - Click "+" → Number
   - **Tags** (multi_select) - Click "+" → Multi-select
   - **Status** (select) - Click "+" → Select
     - Add options: Completed, In Progress, Planned

### 3. Share Database with Integration

1. Click the **"..."** menu in the top right of your database
2. Scroll down and click **"Add connections"**
3. Select your integration
4. Click **"Confirm"**

### 4. Get Database ID

From your database URL:
```
https://www.notion.so/workspace/abc123def456?v=xyz789
                              ^^^^^^^^^^^^
                              This is your database ID
```

Or use the full URL and extract the 32-character ID (remove hyphens).

### 5. Configure CLI

Run the interactive setup:
```bash
cd cli
python -m spearmint_cli.main notion setup
```

Or manually add to `cli/.env`:
```bash
NOTION_API_KEY=secret_your_api_key_here
NOTION_DATABASE_ID=your_database_id_here
```

## Usage

### Add Work Entry
```bash
# Simple entry
spearmint notion add "Fixed authentication bug"

# With details
spearmint notion add "Implemented user dashboard" \
  --desc "Created React components and API endpoints" \
  --duration 3.5 \
  --tags "frontend,react,api" \
  --status "Completed"

# Backdate entry
spearmint notion add "Code review" \
  --date 2025-12-01 \
  --duration 1.5
```

### List Entries
```bash
# Last 7 days (default)
spearmint notion list

# Last 30 days
spearmint notion list --days 30

# Filter by tags
spearmint notion list --tags "frontend,react"

# Limit results
spearmint notion list --limit 10
```

### Search Databases
```bash
# List all databases
spearmint notion search-db

# Search by name
spearmint notion search-db "Work History"
```

## Periodic Tracking

### Using Cron (Linux/Mac)

Add to crontab (`crontab -e`):
```bash
# Every day at 5 PM, prompt for work summary
0 17 * * * cd /path/to/project/cli && python -m spearmint_cli.main notion add "$(read -p 'Work summary: ' summary && echo $summary)"

# Or use a wrapper script
0 17 * * * /path/to/project/scripts/log_work.sh
```

### Using Task Scheduler (Windows)

Create `scripts/log_work.bat`:
```batch
@echo off
cd C:\path\to\project\cli
python -m spearmint_cli.main notion add "Daily work log" --desc "Auto-generated entry"
```

Schedule in Task Scheduler to run daily.

### Using Git Hooks

Create `.git/hooks/post-commit`:
```bash
#!/bin/bash
# Log commit as work entry
COMMIT_MSG=$(git log -1 --pretty=%B)
cd cli
python -m spearmint_cli.main notion add "Commit: $COMMIT_MSG" --tags "git,commit"
```

Make executable: `chmod +x .git/hooks/post-commit`

## API Reference

Based on Notion API v2022-06-28:

### Key Endpoints Used

- **POST /v1/pages** - Create work entry
- **POST /v1/databases/{id}/query** - Query entries with filters
- **PATCH /v1/pages/{id}** - Update entry
- **POST /v1/search** - Search databases

### Authentication

All requests require:
```
Authorization: Bearer {your_api_key}
Notion-Version: 2022-06-28
```

## Troubleshooting

### "Unauthorized" Error
- Verify your API key is correct
- Check that the integration has access to the database
- Ensure you shared the database with your integration

### "Database not found"
- Verify the database ID is correct (32 characters, no hyphens)
- Check that the database wasn't deleted or moved
- Use `spearmint notion search-db` to find your database

### "Invalid property"
- Ensure your database has all required properties
- Property names are case-sensitive
- Check property types match (e.g., "Date" must be a date property)

## Advanced Usage

### Custom Automation Script

Create `scripts/daily_log.py`:
```python
#!/usr/bin/env python3
from spearmint_cli.notion_client import NotionClient
from datetime import datetime

client = NotionClient()

# Prompt for work summary
title = input("What did you work on today? ")
description = input("Details (optional): ")
duration = input("Hours spent (optional): ")

client.create_work_entry(
    title=title,
    description=description or "No details provided",
    duration=float(duration) if duration else None,
    tags=["daily-log"],
    status="Completed"
)

print("✓ Work logged to Notion!")
```

Run daily: `python scripts/daily_log.py`

## Resources

- [Notion API Documentation](https://developers.notion.com/)
- [Postman Collection](https://www.postman.com/notionhq/notion-s-api-workspace/collection/y28pjg6/notion-api)
- [Notion API Reference](https://developers.notion.com/reference/intro)
