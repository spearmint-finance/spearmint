# Product Requirements Document: Tiller Money Integration

**Product:** Spearmint Personal Finance Engine
**Feature:** Tiller Money Direct Integration
**Owner:** Product Team
**Status:** Draft - Ready for Review
**Last Updated:** 2026-02-04

---

## Executive Summary

Spearmint currently requires users to manually export transaction data from their financial tracking tools and upload Excel files to import transactions. This creates friction and reduces the value of having real-time financial analysis.

**Tiller Money** is a popular service that automatically pulls bank transactions into **Google Sheets** or **Microsoft Excel** using Yodlee and Plaid aggregators. Many Spearmint users already use Tiller to aggregate their bank data. By integrating directly with Tiller-powered spreadsheets, we can eliminate manual exports and enable automatic or one-click transaction syncing.

**Platform Support:**
- **Google Sheets** - Auto-fill enabled, stored in Google Drive
- **Microsoft Excel** - Manual fill via add-in, stored on OneDrive or locally

**Expected Impact:**
- Eliminate manual export/upload workflow for Tiller users
- Enable automatic daily transaction syncing
- Reduce time-to-insight for financial analysis
- Position Spearmint as a powerful analysis layer on top of Tiller's data aggregation

---

## Problem Statement

### The User Problem

Users who use Tiller Money to aggregate their bank transactions face a tedious workflow to get data into Spearmint:

1. Open Tiller Google Sheet
2. Export Transactions sheet to Excel/CSV
3. Open Spearmint Import page
4. Upload the file
5. Wait for processing
6. Repeat every time they want updated data

This manual process:
- Takes 5-10 minutes per sync
- Discourages frequent updates
- Creates stale data in Spearmint
- Introduces human error (wrong date ranges, forgetting to sync)

### The Technical Problem

1. **No direct Tiller API** - Tiller doesn't expose a public API; data lives in user's Google Sheets
2. **Google OAuth complexity** - Accessing user's sheets requires OAuth consent flow
3. **Column mapping** - Tiller's column structure differs from Spearmint's import format
4. **Incremental sync** - Need to track what's already imported to avoid duplicates
5. **Rate limits** - Google Sheets API has quotas that must be respected

### Evidence

**User Signals:**
- Multiple users mention using Tiller in support conversations
- Feature requests for "automatic bank sync" or "connect to banks"
- Users asking about Plaid integration (Tiller already handles this)

**Market Context:**
- Tiller has 100k+ users for bank-to-spreadsheet automation
- Tiller costs $79/year - users are invested in the ecosystem
- No self-hosted PFM tools integrate with Tiller currently

---

## Goals & Success Metrics

### Goals

1. **Eliminate manual workflow:** Users can sync Tiller transactions with one click
2. **Enable automation:** Support scheduled automatic syncing (daily/hourly)
3. **Preserve flexibility:** Users can still manually import if needed
4. **Maintain data integrity:** No duplicate transactions, proper categorization

### Success Metrics

| Metric | Target | Timeframe |
|--------|--------|-----------|
| % of users connecting Tiller | 15% | 3 months post-launch |
| Avg. manual imports per user (reduction) | -70% | 3 months post-launch |
| Tiller sync success rate | 99% | Ongoing |
| Avg. sync time | <30 seconds | Launch |
| User satisfaction (Tiller feature) | 4.5/5 | 3 months post-launch |

---

## How Tiller Works

### Data Flow Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Bank Accounts  │────►│  Yodlee/Plaid   │────►│  Tiller Cloud   │
│  (User's banks) │     │  (Aggregators)  │     │  (Orchestrator) │
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                         │
                                        ┌────────────────┴────────────────┐
                                        │                                 │
                                        ▼                                 ▼
                               ┌─────────────────┐               ┌─────────────────┐
                               │  Google Sheets  │               │  Microsoft Excel│
                               │  (Google Drive) │               │  (OneDrive/Local)│
                               │                 │               │                 │
                               │  Auto-fill      │               │  Manual fill    │
                               │  every ~6 hours │               │  via add-in     │
                               └────────┬────────┘               └────────┬────────┘
                                        │                                 │
                                   NEW  │ Google                     NEW  │ Microsoft
                                        │ Sheets API                      │ Graph API
                                        │                                 │ (OneDrive)
                                        └────────────────┬────────────────┘
                                                         │
                                                         ▼
                                                ┌─────────────────┐
                                                │   Spearmint     │
                                                │                 │
                                                │  - Analysis     │
                                                │  - Projections  │
                                                │  - AI Insights  │
                                                └─────────────────┘
```

### Platform Differences

| Feature | Google Sheets | Microsoft Excel |
|---------|---------------|-----------------|
| **Data refresh** | Auto-fill every ~6 hours | Manual "Fill" button |
| **Storage** | Google Drive (cloud only) | OneDrive or local |
| **API access** | Google Sheets API | Microsoft Graph API (OneDrive only) |
| **Local files** | N/A | Requires manual upload to Spearmint |
| **Add-in** | Tiller Money Feeds (Sheets) | Tiller Money Feeds (Excel) |

### Tiller Update Frequency

**Google Sheets:**
- Tiller syncs bank data approximately **once per day** (via Yodlee)
- Plaid connections may refresh every few hours
- **Auto-fill** is enabled by default - new data appears automatically (~every 6 hours)
- Users can manually trigger refresh from Tiller Console (Yodlee only)

**Microsoft Excel:**
- Same bank sync frequency as Google Sheets
- **NO auto-fill** - user must click "Fill" button in the Tiller add-in
- Data only appears in workbook after user manually fills
- This means Spearmint can only sync what the user has already filled

**Implication for Spearmint:**
- Google Sheets users can have fully automatic sync (Tiller auto-fills → Spearmint auto-syncs)
- Excel users need to: (1) Click Fill in Tiller, then (2) Click Sync in Spearmint

### Tiller Sheet Structure

**Transactions Sheet Columns:**

| Column | Description | Spearmint Mapping |
|--------|-------------|-------------------|
| `Date` | Transaction date (posted or transaction) | `transaction_date` |
| `Description` | Cleaned merchant description | `description` |
| `Category` | User-assigned category | `category_name` (create if needed) |
| `Amount` | + income, - expense | `amount` + derive `transaction_type` |
| `Account` | Account name/nickname | `account_name` (link to Account) |
| `Account #` | Last 4 digits | `account_number` |
| `Institution` | Bank name | `institution_name` |
| `Month` | First of month | (derived from Date) |
| `Full Description` | Raw bank description | `original_description` |
| `Transaction ID` | Tiller's unique ID | `external_transaction_id` |
| `Account ID` | Tiller's account ID | `external_account_id` |
| `Check Number` | Check # if applicable | `check_number` |
| `Date Added` | When added to sheet | `source_created_at` |
| `Note` | User notes | `notes` |
| `Tags` | User tags | `tags` |

**Balance History Sheet Columns:**

| Column | Description | Spearmint Mapping |
|--------|-------------|-------------------|
| `Date` | Balance date | `balance_date` |
| `Account` | Account name | `account_name` |
| `Balance` | Account balance | `balance` |
| `Institution` | Bank name | `institution_name` |

---

## Integration Options Analysis

### Option 1: Google Sheets API (Recommended)

**Approach:** User authorizes Spearmint to read their Tiller Google Sheet. Spearmint pulls transactions directly via Google Sheets API.

**Pros:**
- Direct access to user's existing Tiller data
- Works with any Tiller template/customization
- No dependency on Tiller company
- User controls access via Google OAuth

**Cons:**
- Requires Google OAuth implementation
- User must share their sheet URL
- Google API rate limits (100 requests/100 seconds/user)

**Implementation:**
1. User clicks "Connect Tiller" in Spearmint
2. OAuth consent flow for Google Sheets read access
3. User pastes their Tiller spreadsheet URL
4. Spearmint validates sheet structure
5. Initial full sync + incremental syncs thereafter

### Option 2: Google Apps Script Bridge

**Approach:** User installs a Google Apps Script in their Tiller sheet that pushes data to Spearmint API.

**Pros:**
- Push-based (real-time when Tiller updates)
- No OAuth in Spearmint (user manages script)

**Cons:**
- Requires user to install/maintain script
- More complex user setup
- Script must authenticate to Spearmint API

**Verdict:** More friction than Option 1. Consider as advanced option later.

### Option 3: Direct Plaid Integration (Future)

**Approach:** Bypass Tiller entirely; connect directly to Plaid.

**Pros:**
- Full control over data flow
- Real-time transaction access
- No Google dependency

**Cons:**
- Duplicates Tiller's functionality
- Plaid costs money ($0.30-$0.50 per connection/month)
- Users would need to re-link all accounts
- Significant implementation effort

**Verdict:** Out of scope for MVP. Consider if Tiller integration proves successful and users want more direct control.

### Option 4: Microsoft Graph API (Excel on OneDrive)

**Approach:** For Excel users who store their Tiller workbook on OneDrive, use Microsoft Graph API to read the workbook.

**Pros:**
- Covers Excel users (significant portion of Tiller base)
- Similar OAuth flow to Google
- Can read Excel files directly from OneDrive

**Cons:**
- Separate OAuth implementation (Microsoft vs Google)
- Excel users with local files still need manual upload
- Excel doesn't auto-fill like Google Sheets (user must click "Fill" first)

**Implementation:**
1. User clicks "Connect Tiller (Excel)"
2. Microsoft OAuth consent flow
3. User selects workbook from OneDrive
4. Spearmint validates and syncs

### Recommendation: Option 1 + Option 4 (Both Platforms)

**Primary:** Google Sheets API for Google Sheets users
**Secondary:** Microsoft Graph API for Excel/OneDrive users
**Fallback:** Manual file upload for Excel users with local files

This covers all Tiller users:
- **Google Sheets users** → Google Sheets API (auto-sync capable)
- **Excel + OneDrive users** → Microsoft Graph API (manual sync)
- **Excel + Local files** → Enhanced file upload (Tiller format detection)

---

## User Stories

### Primary User Stories

**As a Tiller user, I want to:**

1. **Connect my Tiller sheet** so Spearmint can access my transactions
   - *Acceptance:* OAuth flow completes, sheet validates, test read succeeds

2. **Sync all transactions** on first connection for historical analysis
   - *Acceptance:* Full sync imports all transactions with proper categorization

3. **See new transactions automatically** without manual action
   - *Acceptance:* Scheduled sync runs daily (configurable)

4. **Manually trigger a sync** when I know Tiller has new data
   - *Acceptance:* "Sync Now" button fetches latest transactions

5. **See sync status and history** so I know if syncing is working
   - *Acceptance:* Dashboard shows last sync time, success/failure, count

6. **Map Tiller categories to Spearmint categories** for proper analysis
   - *Acceptance:* Category mapping UI allows 1:1 or many:1 mapping

7. **Handle new accounts automatically** when I add banks in Tiller
   - *Acceptance:* New accounts create Spearmint Account records

### Secondary User Stories

**As a Tiller user, I want to:**

8. **Disconnect Tiller** if I no longer want automatic sync
   - *Acceptance:* Revoke access, stop syncing, keep imported data

9. **Re-authorize** if my Google token expires
   - *Acceptance:* Prompt to re-auth, resume syncing

10. **See sync errors** and understand what went wrong
    - *Acceptance:* Error messages explain issue and remediation

---

## UI/UX Design

### Where It Lives

The Tiller integration will be accessible from:

1. **Settings > Integrations** (new tab) - Primary configuration location
2. **Import page** - As an alternative to file upload
3. **Dashboard** - Sync status indicator

### Settings > Integrations Page

```
┌─────────────────────────────────────────────────────────────────┐
│  Settings                                                        │
├─────────────────────────────────────────────────────────────────┤
│  [Categories] [Classifications] [API Keys] [Integrations]       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  TILLER MONEY                                    [Connected] ││
│  │  ─────────────────────────────────────────────────────────  ││
│  │                                                              ││
│  │  📊 Spreadsheet: "Tiller Money - 2026"                       ││
│  │  📅 Last Sync: 2 hours ago (245 transactions)                ││
│  │  🔄 Auto-Sync: Daily at 6:00 AM                              ││
│  │                                                              ││
│  │  [Sync Now]  [View History]  [Settings]  [Disconnect]        ││
│  │                                                              ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  OTHER INTEGRATIONS                              [Coming Soon]││
│  │  ─────────────────────────────────────────────────────────  ││
│  │                                                              ││
│  │  • Plaid Direct (Q3 2026)                                    ││
│  │  • Monarch Money Import                                      ││
│  │  • YNAB Import                                               ││
│  │                                                              ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Connection Flow (First-Time Setup)

```
Step 1: Choose Platform
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│  🌿 Connect Tiller Money                                         │
│                                                                  │
│  Automatically sync your bank transactions from Tiller to       │
│  Spearmint. No more manual exports!                             │
│                                                                  │
│  Which platform do you use with Tiller?                         │
│                                                                  │
│  ┌─────────────────────────┐  ┌─────────────────────────┐       │
│  │   📊 Google Sheets      │  │   📗 Microsoft Excel    │       │
│  │                         │  │                         │       │
│  │   Auto-sync supported   │  │   OneDrive or Local     │       │
│  │   (recommended)         │  │                         │       │
│  │                         │  │                         │       │
│  │   [Connect Google]      │  │   [Connect Microsoft]   │       │
│  └─────────────────────────┘  └─────────────────────────┘       │
│                                                                  │
│  📁 Have a local Excel file? [Upload directly instead]          │
│                                                                  │
│  🔒 Spearmint only requests read-only access. We never          │
│     modify your Tiller data.                                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

Step 2a: Google OAuth (if Google Sheets selected)
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│  [Google OAuth Consent Screen]                                  │
│                                                                  │
│  "Spearmint wants to:"                                          │
│  • View your Google Sheets files                                │
│                                                                  │
│  [Allow]  [Cancel]                                              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

Step 2b: Microsoft OAuth (if Excel selected)
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│  [Microsoft OAuth Consent Screen]                               │
│                                                                  │
│  "Spearmint wants to:"                                          │
│  • Read your OneDrive files                                     │
│                                                                  │
│  [Accept]  [Cancel]                                             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

Step 3: Sheet/Workbook Selection
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│  📋 Select Your Tiller Spreadsheet                               │
│                                                                  │
│  Paste your Tiller spreadsheet URL:                             │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ https://docs.google.com/spreadsheets/d/1abc123.../edit      ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  Or select from your recent sheets:                             │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ ○ Tiller Money - 2026                     Last edited: Today││
│  │ ○ Tiller Budget 2025                      Last edited: Dec  ││
│  │ ○ Family Finances                         Last edited: Nov  ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  [Validate & Continue]                                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

Step 2: Google OAuth
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│  [Google OAuth Consent Screen]                                  │
│                                                                  │
│  "Spearmint wants to:"                                          │
│  • View your Google Sheets files                                │
│                                                                  │
│  [Allow]  [Cancel]                                              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

Step 3: Sheet Selection
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│  📋 Select Your Tiller Spreadsheet                               │
│                                                                  │
│  Paste your Tiller spreadsheet URL:                             │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ https://docs.google.com/spreadsheets/d/1abc123.../edit      ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  Or select from your recent sheets:                             │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ ○ Tiller Money - 2026                     Last edited: Today││
│  │ ○ Tiller Budget 2025                      Last edited: Dec  ││
│  │ ○ Family Finances                         Last edited: Nov  ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  [Validate & Continue]                                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

Step 4: Validation & Initial Sync
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│  ✓ Validating sheet structure...                                │
│  ✓ Found Transactions sheet with 1,247 rows                     │
│  ✓ Found Balance History sheet                                  │
│  ✓ Detected 5 accounts                                          │
│                                                                  │
│  Ready to import:                                                │
│  • 1,247 transactions (Jan 2024 - Feb 2026)                     │
│  • 5 accounts (checking, savings, 3 credit cards)               │
│  • 45 categories                                                │
│                                                                  │
│  [Start Initial Sync]                                           │
│                                                                  │
│  ⏱️ This may take 1-2 minutes for large datasets                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

Step 5: Sync Progress
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│  📥 Importing Transactions...                                    │
│                                                                  │
│  ████████████████████░░░░░░░░░░  65%                            │
│                                                                  │
│  • Processed: 810 / 1,247 transactions                          │
│  • New accounts created: 5                                       │
│  • New categories created: 12                                    │
│  • Duplicates skipped: 0                                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

Step 6: Complete
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│  ✅ Tiller Connected Successfully!                               │
│                                                                  │
│  Imported:                                                       │
│  • 1,247 transactions                                           │
│  • 5 accounts                                                   │
│  • 45 categories                                                │
│                                                                  │
│  Auto-Sync Schedule:                                             │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ ○ Every hour                                                 ││
│  │ ● Every day at 6:00 AM (Recommended)                         ││
│  │ ○ Manual only                                                ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  [Go to Dashboard]  [Configure Category Mapping]                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Import Page Enhancement

Add Tiller as an import source alongside file upload:

```
┌─────────────────────────────────────────────────────────────────┐
│  Import Transactions                                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Choose import source:                                           │
│                                                                  │
│  ┌───────────────────────┐  ┌───────────────────────┐           │
│  │   📄                   │  │   🌿                   │           │
│  │   Upload File          │  │   Tiller Money         │           │
│  │                        │  │                        │           │
│  │   Excel, CSV           │  │   [Connected ✓]        │           │
│  │                        │  │   Last sync: 2h ago    │           │
│  │   [Upload]             │  │   [Sync Now]           │           │
│  └───────────────────────┘  └───────────────────────┘           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Dashboard Sync Status

Add a small indicator to the dashboard header:

```
┌─────────────────────────────────────────────────────────────────┐
│  Dashboard                                    Tiller: ✓ 2h ago  │
├─────────────────────────────────────────────────────────────────┤
│  ...                                                            │
```

Clicking opens a popover with sync details and "Sync Now" button.

---

## Technical Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────────┐
│                         Spearmint                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Frontend (React)                                                │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  IntegrationsPage.tsx     TillerConnect.tsx                  ││
│  │  TillerSyncStatus.tsx     CategoryMappingDialog.tsx          ││
│  └─────────────────────────────────────────────────────────────┘│
│                           │                                      │
│                           ▼                                      │
│  Backend (FastAPI)                                               │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  /api/integrations/tiller/                                   ││
│  │    POST   /connect      - Initiate OAuth                     ││
│  │    GET    /callback     - OAuth callback                     ││
│  │    POST   /validate     - Validate sheet structure           ││
│  │    POST   /sync         - Trigger manual sync                ││
│  │    GET    /status       - Get sync status                    ││
│  │    GET    /history      - Get sync history                   ││
│  │    DELETE /disconnect   - Remove connection                  ││
│  │                                                              ││
│  │  TillerService                                               ││
│  │    - OAuth token management                                  ││
│  │    - Sheet reading via Google Sheets API                     ││
│  │    - Transaction transformation                              ││
│  │    - Incremental sync logic                                  ││
│  └─────────────────────────────────────────────────────────────┘│
│                           │                                      │
│                           ▼                                      │
│  Database                                                        │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  TillerConnection       TillerSyncHistory                    ││
│  │  - google_refresh_token - sync_id                            ││
│  │  - spreadsheet_id       - started_at                         ││
│  │  - last_sync_at         - completed_at                       ││
│  │  - sync_schedule        - transactions_synced                ││
│  │  - is_active            - status                             ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Google Sheets API                             │
│                                                                  │
│  - OAuth 2.0 authorization                                       │
│  - spreadsheets.values.get (read rows)                          │
│  - Rate limit: 100 requests/100 seconds/user                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Database Models

```python
# New models in models.py

class TillerConnection(Base):
    """Stores Tiller Google Sheets connection configuration."""
    __tablename__ = "tiller_connections"

    connection_id = Column(Integer, primary_key=True, autoincrement=True)
    spreadsheet_id = Column(String(100), nullable=False)  # Google Sheet ID
    spreadsheet_name = Column(String(255), nullable=True)
    google_refresh_token = Column(String(512), nullable=False)  # Encrypted
    transactions_sheet_name = Column(String(100), default="Transactions")
    balance_sheet_name = Column(String(100), default="Balance History")

    # Sync configuration
    sync_schedule = Column(String(20), default="daily")  # hourly, daily, manual
    sync_time = Column(Time, nullable=True)  # For daily schedule
    last_sync_at = Column(DateTime, nullable=True)
    last_sync_row = Column(Integer, default=0)  # For incremental sync

    # Status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)


class TillerSyncHistory(Base):
    """Tracks individual sync operations."""
    __tablename__ = "tiller_sync_history"

    sync_id = Column(Integer, primary_key=True, autoincrement=True)
    connection_id = Column(Integer, ForeignKey("tiller_connections.connection_id"))

    started_at = Column(DateTime, nullable=False)
    completed_at = Column(DateTime, nullable=True)

    # Results
    status = Column(String(20), default="running")  # running, success, failed
    transactions_found = Column(Integer, default=0)
    transactions_imported = Column(Integer, default=0)
    transactions_skipped = Column(Integer, default=0)
    accounts_created = Column(Integer, default=0)
    categories_created = Column(Integer, default=0)

    # Error tracking
    error_message = Column(Text, nullable=True)

    # Relationships
    connection = relationship("TillerConnection", backref="sync_history")


class TillerCategoryMapping(Base):
    """Maps Tiller categories to Spearmint categories."""
    __tablename__ = "tiller_category_mappings"

    mapping_id = Column(Integer, primary_key=True, autoincrement=True)
    tiller_category = Column(String(100), nullable=False)  # Category name in Tiller
    spearmint_category_id = Column(Integer, ForeignKey("categories.category_id"))

    # Auto-create behavior
    auto_created = Column(Boolean, default=False)  # Created automatically on sync

    # Relationships
    spearmint_category = relationship("Category")
```

### Sync Algorithm

```python
class TillerSyncService:
    """Handles Tiller transaction synchronization."""

    async def sync_transactions(
        self,
        connection: TillerConnection,
        full_sync: bool = False
    ) -> TillerSyncHistory:
        """
        Sync transactions from Tiller Google Sheet.

        Args:
            connection: TillerConnection instance
            full_sync: If True, sync all transactions. If False, incremental.

        Returns:
            TillerSyncHistory with results
        """
        sync = TillerSyncHistory(
            connection_id=connection.connection_id,
            started_at=utc_now(),
            status="running"
        )

        try:
            # 1. Get Google Sheets client with refreshed token
            sheets_client = await self._get_sheets_client(connection)

            # 2. Read transactions from sheet
            if full_sync:
                start_row = 2  # Skip header
            else:
                start_row = connection.last_sync_row + 1

            transactions_data = await sheets_client.read_range(
                spreadsheet_id=connection.spreadsheet_id,
                range=f"{connection.transactions_sheet_name}!A{start_row}:Z"
            )

            # 3. Transform Tiller rows to Spearmint transactions
            for row in transactions_data:
                transaction = self._transform_row(row, connection)

                # Check for duplicate (by external_transaction_id)
                if self._is_duplicate(transaction):
                    sync.transactions_skipped += 1
                    continue

                # Create account if needed
                if not self._account_exists(transaction.account_name):
                    self._create_account(transaction)
                    sync.accounts_created += 1

                # Map category
                category = self._get_or_create_category(
                    transaction.tiller_category
                )
                if category.auto_created:
                    sync.categories_created += 1

                # Save transaction
                self._save_transaction(transaction, category)
                sync.transactions_imported += 1

            # 4. Update connection state
            connection.last_sync_at = utc_now()
            connection.last_sync_row = start_row + len(transactions_data) - 1

            sync.status = "success"
            sync.completed_at = utc_now()
            sync.transactions_found = len(transactions_data)

        except Exception as e:
            sync.status = "failed"
            sync.error_message = str(e)
            sync.completed_at = utc_now()

        return sync

    def _transform_row(self, row: list, connection: TillerConnection) -> dict:
        """Transform a Tiller sheet row to Spearmint transaction format."""
        # Column indices based on standard Tiller template
        return {
            "transaction_date": parse_date(row[0]),  # Date
            "description": row[1],                    # Description
            "tiller_category": row[2],                # Category
            "amount": Decimal(row[3]),                # Amount
            "transaction_type": "Income" if Decimal(row[3]) > 0 else "Expense",
            "account_name": row[4],                   # Account
            "account_number": row[5],                 # Account #
            "institution": row[6],                    # Institution
            "original_description": row[9] if len(row) > 9 else None,  # Full Description
            "external_transaction_id": row[10] if len(row) > 10 else None,  # Transaction ID
            "notes": row[13] if len(row) > 13 else None,  # Note
        }
```

### Automatic Sync Scheduler

```python
# Using APScheduler or similar

from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()

async def run_scheduled_syncs():
    """Run all due automatic syncs."""
    connections = await get_due_connections()

    for connection in connections:
        try:
            await tiller_service.sync_transactions(connection)
        except Exception as e:
            logger.error(f"Scheduled sync failed for {connection.connection_id}: {e}")

# Add job on startup
scheduler.add_job(
    run_scheduled_syncs,
    'interval',
    minutes=15,  # Check every 15 minutes
    id='tiller_sync_checker'
)
```

### OAuth Configuration

```python
# Google OAuth (for Google Sheets users)
GOOGLE_CLIENT_ID = "xxx.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "xxx"
GOOGLE_REDIRECT_URI = "http://localhost:8000/api/integrations/tiller/google/callback"

GOOGLE_SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly"
]

# Microsoft OAuth (for Excel/OneDrive users)
MICROSOFT_CLIENT_ID = "xxx-xxx-xxx"
MICROSOFT_CLIENT_SECRET = "xxx"
MICROSOFT_REDIRECT_URI = "http://localhost:8000/api/integrations/tiller/microsoft/callback"

MICROSOFT_SCOPES = [
    "Files.Read",           # Read OneDrive files
    "User.Read"             # Get user profile
]
```

### Platform-Specific Considerations

| Platform | Auto-Sync | API | Notes |
|----------|-----------|-----|-------|
| **Google Sheets** | Yes (daily) | Google Sheets API | Tiller auto-fills ~every 6 hours |
| **Excel (OneDrive)** | Manual only | Microsoft Graph API | User must click "Fill" in Tiller first |
| **Excel (Local)** | N/A | File upload | Use enhanced import with Tiller detection |

---

## Security Considerations

### Data Access

| Concern | Mitigation |
|---------|------------|
| Google token storage | Encrypt refresh tokens at rest (AES-256) |
| Token expiry | Refresh access tokens automatically; prompt re-auth if refresh fails |
| Minimal scope | Request only `spreadsheets.readonly` - no write access |
| Sheet validation | Verify sheet structure before syncing; reject non-Tiller sheets |

### User Privacy

- Spearmint never modifies user's Tiller sheet
- Users can disconnect at any time (revokes Google access)
- Sync history retained for audit; can be purged on request
- No Tiller credentials stored (OAuth only)

### Rate Limiting

- Google Sheets API: 100 requests per 100 seconds per user
- Implement exponential backoff on rate limit errors
- Cache sheet metadata to reduce API calls
- Batch reads where possible (read full range, not row-by-row)

---

## Implementation Phases

### Phase 1: Core Connection - Google Sheets (MVP)

**Deliverables:**
- [ ] Google OAuth flow (backend + frontend)
- [ ] Sheet URL input and validation
- [ ] Initial full sync functionality
- [ ] TillerConnection and TillerSyncHistory models
- [ ] Basic Settings > Integrations tab
- [ ] Manual "Sync Now" button
- [ ] Sync status display

**API Endpoints:**
- `POST /api/integrations/tiller/google/connect` - Start Google OAuth
- `GET /api/integrations/tiller/google/callback` - Google OAuth callback
- `POST /api/integrations/tiller/validate` - Validate sheet structure
- `POST /api/integrations/tiller/sync` - Manual sync
- `GET /api/integrations/tiller/status` - Connection status
- `DELETE /api/integrations/tiller/disconnect` - Remove connection

### Phase 1.5: Microsoft Excel/OneDrive Support

**Deliverables:**
- [ ] Microsoft OAuth flow (backend + frontend)
- [ ] OneDrive file picker integration
- [ ] Excel workbook parsing
- [ ] Platform selector in connection flow

**API Endpoints:**
- `POST /api/integrations/tiller/microsoft/connect` - Start Microsoft OAuth
- `GET /api/integrations/tiller/microsoft/callback` - Microsoft OAuth callback

**Note:** Excel users with **local files** (not on OneDrive) should use the standard Import page. We can enhance the import to auto-detect Tiller format.

### Phase 2: Automatic Sync

**Deliverables:**
- [ ] Sync scheduler (hourly/daily options)
- [ ] Incremental sync (only new rows)
- [ ] Background job runner (APScheduler or Celery)
- [ ] Sync schedule configuration UI
- [ ] Dashboard sync status indicator
- [ ] Sync history view

### Phase 3: Category Mapping

**Deliverables:**
- [ ] TillerCategoryMapping model
- [ ] Category mapping UI (map Tiller → Spearmint categories)
- [ ] Auto-create categories option
- [ ] Bulk re-categorization when mapping changes

### Phase 4: Account Sync

**Deliverables:**
- [ ] Read Balance History sheet
- [ ] Create/update Account records from Tiller
- [ ] Sync account balances
- [ ] Account linking UI (match Tiller accounts to existing Spearmint accounts)

### Phase 5: Polish & Reliability

**Deliverables:**
- [ ] Retry logic for failed syncs
- [ ] Notification on sync failure
- [ ] Re-authorization flow when token expires
- [ ] Sync conflict resolution (duplicate detection improvements)
- [ ] Performance optimization (batch inserts)

---

## Open Questions

### Q1: How do we handle Tiller category changes?

**Context:** User might rename a category in Tiller after initial sync.

**Options:**
- A) Ignore - old transactions keep old mapping
- B) Detect renames and prompt user to update mapping
- C) Use Transaction ID to re-sync changed transactions

**Recommendation:** Option A for MVP; consider B for later.

### Q2: Should we support multiple Tiller sheets?

**Context:** Some users have separate sheets for different years or purposes.

**Options:**
- A) Single sheet only (MVP)
- B) Multiple sheets with separate sync settings

**Recommendation:** Option A for MVP; evaluate demand for B.

### Q3: How do we handle Tiller template variations?

**Context:** Tiller has multiple templates; users may customize columns.

**Options:**
- A) Support only "Foundation Template" columns
- B) Column mapping UI for custom setups
- C) Auto-detect columns by header names

**Recommendation:** Option C - auto-detect by header names with fallback to standard positions.

### Q4: What happens to synced data if user disconnects Tiller?

**Options:**
- A) Keep all imported transactions
- B) Offer to delete Tiller-sourced transactions
- C) Mark transactions as "orphaned" but keep

**Recommendation:** Option A - data belongs to user regardless of source.

---

## Success Criteria Checklist

Before marking this feature "complete," we must validate:

**Core Functionality:**
- [ ] User can complete Google OAuth and connect Tiller sheet
- [ ] Initial sync imports all transactions correctly
- [ ] Manual "Sync Now" imports new transactions
- [ ] Duplicate transactions are not created
- [ ] Sync status shows accurate information

**User Experience:**
- [ ] Connection flow completes in under 3 minutes
- [ ] Sync completes in under 60 seconds for 1000 transactions
- [ ] Error messages are clear and actionable
- [ ] Disconnect cleanly revokes access

**Reliability:**
- [ ] Scheduled syncs run on time
- [ ] Failed syncs retry with backoff
- [ ] Token refresh works automatically
- [ ] Rate limits are respected

**Data Integrity:**
- [ ] Transaction amounts match Tiller exactly
- [ ] Dates are correct (handle timezones)
- [ ] Categories map correctly
- [ ] Accounts are created/linked properly

---

## References

**Tiller Documentation:**
- [What is Tiller and how does it work?](https://help.tiller.com/en/articles/3279649-what-is-tiller-and-how-does-it-work)
- [Transactions Sheet Columns](https://help.tiller.com/en/articles/432681-transactions-sheet-columns)
- [Using the Tiller Money Feeds Add-on (Google Sheets)](https://help.tiller.com/en/articles/3278731-using-the-tiller-money-feeds-add-on-for-google-sheets)
- [Using the Tiller Money Feeds Add-in (Microsoft Excel)](https://help.tiller.com/en/articles/2283741-using-the-tiller-money-feeds-add-in-for-microsoft-excel)
- [Getting Started with Tiller for Microsoft Excel](https://help.tiller.com/en/articles/2283680-getting-started-with-tiller-for-microsoft-excel)
- [Tiller for Microsoft Excel FAQ](https://help.tiller.com/en/articles/2267544-tiller-for-microsoft-excel-faq)
- [How often is data added to my spreadsheet](https://help.tiller.com/en/articles/432695-how-often-is-new-data-added-to-my-tiller-powered-spreadsheet)

**Google Sheets API:**
- [Google Sheets API Documentation](https://developers.google.com/sheets/api)
- [OAuth 2.0 for Web Server Applications](https://developers.google.com/identity/protocols/oauth2/web-server)

**Microsoft Graph API:**
- [Microsoft Graph API Documentation](https://learn.microsoft.com/en-us/graph/)
- [OneDrive API - Working with Excel](https://learn.microsoft.com/en-us/graph/api/resources/excel)
- [Microsoft Identity Platform OAuth 2.0](https://learn.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-auth-code-flow)

**Related Spearmint PRDs:**
- [MCP Server PRD](./MCP_SERVER_PRD.md) - Similar OAuth pattern for API keys

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-02-04 | Product Team | Initial draft |

---

## Appendix A: Tiller Column Reference

| Column | Required | Description |
|--------|----------|-------------|
| Date | Yes | Transaction date |
| Description | Yes | Cleaned merchant name |
| Category | No | User-assigned category |
| Amount | Yes | Transaction amount (+/-) |
| Account | Yes | Account name |
| Account # | No | Last 4 digits |
| Institution | No | Bank name |
| Month | No | First of month |
| Week | No | Week start (Sunday) |
| Full Description | No | Raw bank description |
| Transaction ID | Recommended | Tiller's unique ID |
| Account ID | No | Tiller's account ID |
| Check Number | No | If check transaction |
| Date Added | No | When added to sheet |
| Note | No | User notes |
| Tags | No | User tags |

---

## Appendix B: Google OAuth Scopes

```
Requested scopes (minimal):
- https://www.googleapis.com/auth/spreadsheets.readonly
- https://www.googleapis.com/auth/drive.readonly

These allow:
- Reading spreadsheet data
- Listing user's spreadsheets (for selection UI)

These do NOT allow:
- Modifying any data
- Accessing other Google services
- Deleting files
```
