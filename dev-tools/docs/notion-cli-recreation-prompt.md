# Notion CLI Recreation Prompt

Use this prompt to recreate the Notion work history tracking CLI from scratch.

---

## Prompt

I want to create a CLI tool that allows me to periodically save my work history to Notion. 

**Requirements:**

1. **CLI Commands:**
   - `notion add` - Create new work entries with title, description, duration, tags, and status
   - `notion list` - View recent work entries with filtering by date range and tags
   - `notion setup` - Interactive configuration wizard for API key and database ID
   - `notion search-db` - Search for databases in Notion workspace

2. **Notion Integration:**
   - Use the Notion API v2022-06-28
   - Based on the official Notion API collection: https://www.postman.com/notionhq/notion-s-api-workspace/collection/y28pjg6/notion-api
   - Key endpoints to use:
     - `POST /v1/pages` - Create work entries
     - `POST /v1/databases/{id}/query` - Query entries with filters
     - `POST /v1/search` - Search for databases
     - `PATCH /v1/pages/{id}` - Update entries

3. **Database Schema:**
   The Notion database should have these properties:
   - **Title** (title) - Work entry title
   - **Date** (date) - When the work was done
   - **Description** (rich_text) - Detailed description
   - **Duration** (number) - Hours spent
   - **Tags** (multi_select) - Categorization tags
   - **Status** (select) - Completed, In Progress, Planned

4. **Project Structure:**
   ```
   cli/
   ├── .env                          # Environment variables
   ├── setup.py                      # Package setup
   ├── requirements.txt              # Dependencies
   ├── NOTION_SETUP.md              # Setup documentation
   └── src/
       └── spearmint_cli/
           ├── main.py              # CLI entry point with commands
           └── notion_client.py     # Notion API client wrapper
   ```

5. **Technical Stack:**
   - **CLI Framework:** typer (for command-line interface)
   - **Output:** rich (for beautiful terminal output with tables)
   - **HTTP:** requests (for Notion API calls)
   - **Config:** python-dotenv (for environment variables)

6. **Features:**
   - Load API key and database ID from `.env` file
   - Format database IDs correctly (handle with/without hyphens)
   - Display results in formatted tables with colors
   - Show total hours worked
   - Support filtering by date range and tags
   - Provide helpful error messages
   - Include setup wizard for first-time configuration

7. **Environment Variables:**
   ```bash
   NOTION_API_KEY=secret_your_api_key_here
   NOTION_DATABASE_ID=your_32_character_database_id
   ```

8. **Usage Examples:**
   ```bash
   # Add work entry
   python -m spearmint_cli.main notion add "Fixed authentication bug" \
     --desc "Resolved JWT token expiration issue" \
     --duration 2.5 \
     --tags "backend,bugfix" \
     --status "Completed"

   # List recent work
   python -m spearmint_cli.main notion list --days 7

   # Filter by tags
   python -m spearmint_cli.main notion list --tags "frontend,react"

   # Interactive setup
   python -m spearmint_cli.main notion setup

   # Search databases
   python -m spearmint_cli.main notion search-db "Work History"
   ```

9. **Documentation to Include:**
   Create a `NOTION_SETUP.md` file with:
   - Step-by-step Notion integration setup
   - How to get API key from https://www.notion.so/my-integrations
   - How to create and configure the database
   - How to share database with integration
   - How to extract database ID from URL
   - Troubleshooting common issues
   - Examples of periodic tracking (cron, git hooks, etc.)

10. **Helper Script:**
    Create `scripts/log_work.sh` - an interactive bash script that prompts for work details and logs to Notion

**Implementation Notes:**
- Make SDK imports optional so Notion commands work independently
- Format database IDs as UUID with hyphens (8-4-4-4-12 format)
- Handle API errors gracefully with clear error messages
- Use `load_dotenv()` to load environment variables from `.env`
- Add comprehensive error handling for missing credentials
- Display Notion URLs in success messages
- Support both absolute and relative date filtering

**Expected Output:**
A fully functional CLI that integrates with Notion API to track work history, with beautiful terminal output, comprehensive documentation, and easy setup process.

---

## Additional Context

The CLI should be part of an existing project structure where:
- Main CLI is at `cli/src/spearmint_cli/main.py`
- It may have other commands (like `status`, `balances`, etc.) that use a different SDK
- The Notion commands should be added as a subcommand group using `typer.Typer()`
- Dependencies are listed in `cli/requirements.txt`
- Installation uses `pip install -e .` with a `setup.py` file

## Setup Instructions to Include

1. **Create Notion Integration:**
   - Go to https://www.notion.so/my-integrations
   - Create new integration
   - Copy API key (starts with `secret_` or `ntn_`)

2. **Create Database:**
   - Create new page in Notion
   - Add database with required properties
   - Share database with integration (click "..." → "Connections" → Add your integration)

3. **Get Database ID:**
   - Open database in Notion
   - Copy URL: `https://www.notion.so/Database-Name-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX?v=...`
   - Extract the 32-character ID (the X's)

4. **Configure CLI:**
   - Add credentials to `cli/.env`
   - Run setup wizard: `python -m spearmint_cli.main notion setup`

5. **Test:**
   - Add test entry: `python -m spearmint_cli.main notion add "Test"`
   - List entries: `python -m spearmint_cli.main notion list`

---

## Key Implementation Details

### Notion Client (`notion_client.py`)
- Class-based API wrapper
- Methods: `create_work_entry()`, `query_entries()`, `update_entry()`, `search_database()`
- Automatic database ID formatting (add hyphens if missing)
- Proper error handling with response details

### CLI Commands (`main.py`)
- Use `@notion_app.command()` decorators
- Rich console output with colors and tables
- Progress indicators with `console.status()`
- Argument parsing with typer (Arguments for required, Options for optional)

### Error Handling
- Check for missing environment variables
- Validate database ID format (32 characters)
- Display Notion API error messages
- Provide actionable troubleshooting steps

### Output Formatting
- Use Rich tables for list view
- Color coding: green for success, red for errors, yellow for warnings
- Show total hours worked
- Display Notion URLs for created entries
- Truncate long text in tables

---

Use this prompt with an AI assistant to recreate the entire Notion CLI integration from scratch.
