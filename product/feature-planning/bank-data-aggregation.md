# Product Requirements Document: Bank Data Aggregation

**Product:** Spearmint Personal Finance Engine
**Feature:** Direct Bank Account Linking via Plaid
**Owner:** Accounts Team
**Status:** Draft
**Last Updated:** 2026-03-15

---

## Executive Summary

Spearmint currently requires users to manually upload Excel files exported from their banking tools to import accounts and transactions. This creates a tedious, error-prone workflow that discourages frequent data updates and results in stale financial analysis. Users want their bank data to flow into Spearmint automatically.

This PRD defines the integration of **Plaid** as Spearmint's primary bank data aggregation provider. Plaid enables users to securely link their bank accounts and automatically sync transactions, balances, and investment holdings — eliminating the manual export/upload cycle entirely.

**Why Plaid over Yodlee:** After evaluating both platforms (see [Appendix A](#appendix-a-plaid-vs-yodlee-evaluation)), Plaid is recommended for Spearmint because of its significantly lower barrier to entry (self-serve signup, no enterprise sales process), faster integration timeline (1-2 weeks vs 4-8 weeks), better developer experience (official Python and React SDKs), per-link pricing that scales with a small user base ($0.50-$2.00/link vs Yodlee's $8K-$15K/month minimums), and proven track record with personal finance applications (YNAB, Copilot Money, Monarch). While Yodlee offers slightly broader international coverage and richer investment account subtypes, these advantages do not justify the 10-30x cost premium and longer integration cycle for Spearmint's current scale.

**Expected Impact:**
- Eliminate 5-10 minute manual export/upload workflow per sync
- Enable automatic daily transaction syncing for linked accounts
- Reduce time-to-insight from "hours/days" to "seconds" for new transactions
- Support 12,000+ financial institutions covering ~95% of US banks
- Enable real account balance tracking (vs. manually entered snapshots)
- Position Spearmint alongside modern PFM tools that offer direct bank linking

---

## Problem Statement

### The User Problem

Today's data import workflow creates friction at every step:

1. **Manual export:** Users must log into their bank, export transactions to Excel/CSV, then upload to Spearmint. This takes 5-10 minutes per bank account, per sync.

2. **Stale data:** Because syncing is manual, most users sync infrequently. Financial analysis is only as good as the last import — often days or weeks old.

3. **Error-prone:** Manual exports introduce human error: wrong date ranges, missed accounts, duplicate imports, column mapping issues.

4. **No real-time balances:** Account balances in Spearmint are based on manually entered snapshots or calculated from imported transactions. Users can't see their actual bank balance.

5. **No investment holdings sync:** Investment positions (stocks, bonds, mutual funds) must be manually entered as holdings. No automatic portfolio tracking.

6. **Incomplete account picture:** Users with accounts at multiple institutions must repeat the export/upload process for each one, discouraging comprehensive financial tracking.

### The Technical Problem

1. **No bank connectivity layer:** Spearmint has no mechanism to connect directly to financial institutions.
2. **No credential management:** Securely storing and refreshing bank authentication is complex (MFA, OAuth, session management).
3. **No webhook infrastructure:** Receiving real-time notifications when new transactions are available requires webhook handling.
4. **Account-transaction linkage gap:** The current transaction schema doesn't enforce `account_id` on transactions (KI-001), which must be addressed for linked accounts where every transaction belongs to a specific account.

### Evidence

- The Tiller Integration PRD (`product/TILLER_INTEGRATION_PRD.md`) was created to solve this same problem via a spreadsheet intermediary, validating user demand for automatic syncing.
- Users asking about "connect to banks" and "Plaid integration" in feedback.
- Every major PFM competitor (Monarch, YNAB, Copilot Money, Lunch Money) offers direct bank linking via Plaid.
- The existing import flow (`/import` endpoint) processes Excel files only — no API-based data ingestion path exists.

---

## Goals & Success Metrics

### Goals

1. **Eliminate manual workflow:** Users link accounts once and get transactions automatically going forward.
2. **Real-time balance tracking:** Display actual bank balances, not manually entered snapshots.
3. **Investment portfolio sync:** Automatically pull holdings, quantities, and current values for investment accounts.
4. **Maintain backward compatibility:** File-based import continues to work for users who prefer it or whose institutions aren't supported.
5. **Data integrity:** No duplicate transactions, proper account association, accurate categorization.

### Success Metrics

| Metric | Target | Timeframe |
|--------|--------|-----------|
| % of users linking at least one account | 30% | 3 months post-launch |
| Manual imports per user (reduction) | -80% | 3 months post-launch |
| Plaid link success rate | 95% | Ongoing |
| Transaction sync latency (webhook → available) | <60 seconds | Launch |
| Investment holdings accuracy | 99% | Ongoing |
| User satisfaction (bank linking feature) | 4.5/5 | 3 months post-launch |

---

## User Stories

### Primary Stories

**US-1: Link a bank account**
> As a user, I want to securely connect my bank account to Spearmint so that my transactions sync automatically.

Acceptance criteria:
- User clicks "Link Account" and sees the Plaid Link modal
- User selects their bank, enters credentials, completes MFA
- On success, the linked account appears in the Accounts page with correct name, type, institution, and last 4 digits
- Initial transaction history (up to 2 years) begins importing
- User can link multiple accounts from the same or different institutions

**US-2: View synced transactions**
> As a user, I want to see my bank transactions appear in Spearmint automatically so I don't have to manually import them.

Acceptance criteria:
- Transactions from linked accounts appear in the Transactions page
- New transactions arrive within 24 hours of posting at the bank
- Each transaction shows: date, description, amount, category, account name
- Plaid-provided categories are mapped to Spearmint categories
- No duplicate transactions on repeated syncs

**US-3: View real-time balance**
> As a user, I want to see my actual bank balance on my account card so I know my current financial position.

Acceptance criteria:
- Linked account cards show the latest balance from Plaid
- Balance updates when Plaid refreshes (1-4x daily)
- Balance history is automatically populated from Plaid snapshots
- Net worth calculation uses live balances from linked accounts

**US-4: Sync investment holdings**
> As a user, I want my brokerage and retirement account holdings to sync automatically so I can track my investment portfolio.

Acceptance criteria:
- For linked investment accounts (brokerage, 401k, IRA), holdings are automatically populated
- Each holding shows: symbol, description, quantity, cost basis, current value
- Gain/loss calculations are based on Plaid-provided cost basis and current value
- Holdings update daily with market prices

**US-5: Manage linked accounts**
> As a user, I want to disconnect a bank account or re-authenticate when my login changes so I stay in control of my data.

Acceptance criteria:
- User can unlink an account from the Account Details dialog
- Unlinking removes the Plaid connection but preserves imported transactions
- When Plaid detects an auth error, user sees a banner prompting re-authentication
- Re-authentication uses Plaid Link in update mode

### Secondary Stories (Phase 2+)

**US-6: Automatic categorization improvement**
> As a user, I want Plaid's merchant categorization to seed Spearmint's category rules so that new transactions are auto-categorized more accurately.

**US-7: Transfer detection across linked accounts**
> As a user, I want Spearmint to automatically detect transfers between my linked accounts (e.g., checking → savings) and mark them accordingly.

**US-8: Scheduled balance snapshots**
> As a user, I want daily balance snapshots recorded automatically so I can see my balance history chart without manual entry.

---

## Functional Requirements

### FR-1: Plaid Link Integration (Frontend)

Integrate the Plaid Link React SDK to handle the account linking flow.

**Flow:**
```
User clicks "Link Account"
    ↓
Frontend calls POST /api/plaid/link-token
    ↓
Backend creates link_token via Plaid API
    ↓
Frontend opens Plaid Link with link_token
    ↓
User selects institution, enters credentials, completes MFA
    ↓
Plaid Link returns public_token + metadata (accounts, institution)
    ↓
Frontend sends public_token to POST /api/plaid/exchange-token
    ↓
Backend exchanges public_token for access_token via Plaid API
    ↓
Backend stores encrypted access_token, creates Account records
    ↓
Backend triggers initial transaction sync
    ↓
Frontend refreshes account list
```

**Plaid Link Configuration:**
- Products: `transactions`, `investments`, `liabilities`
- Country codes: `US`
- Account types: all (checking, savings, credit card, loan, brokerage, 401k, IRA)
- Language: English

### FR-2: Token Management (Backend)

Securely store and manage Plaid access tokens.

| Field | Storage | Notes |
|-------|---------|-------|
| `access_token` | Encrypted at rest (AES-256) | Never exposed to frontend |
| `item_id` | PlaidItem table | Plaid's identifier for the connection |
| `institution_id` | PlaidItem table | For display purposes |
| `consent_expiration` | PlaidItem table | Track when re-consent needed |
| `cursor` | PlaidItem table | For incremental `/transactions/sync` |
| `error_code` | PlaidItem table | Track auth errors for re-link prompts |

### FR-3: Transaction Sync (Backend)

Use Plaid's `/transactions/sync` endpoint for incremental transaction syncing.

**Initial sync:** Pull up to 2 years of transaction history after account linking.

**Ongoing sync:** Use cursor-based incremental sync to efficiently pull only new/modified/removed transactions.

**Webhook-driven:** Register for `SYNC_UPDATES_AVAILABLE` webhook to trigger syncs when Plaid has new data (1-4x daily).

**Transaction mapping:**

| Plaid Field | Spearmint Field | Transformation |
|-------------|-----------------|----------------|
| `transaction_id` | `external_transaction_id` | Direct mapping |
| `date` | `transaction_date` | ISO date |
| `amount` | `amount` | Plaid: positive = money out; Spearmint: store absolute value |
| `amount` (sign) | `transaction_type` | Positive → Expense, Negative → Income |
| `name` | `description` | Cleaned merchant name |
| `merchant_name` | `source` | Original merchant |
| `personal_finance_category.primary` | `category_name` | Map to Spearmint category (create if needed) |
| `account_id` | `account_id` | Via PlaidItem → Account lookup |
| `pending` | `is_cleared` | `pending=true` → `is_cleared=false` |
| `payment_channel` | `payment_method` | in_store, online, other |

**Deduplication:** Use `transaction_id` as the unique external identifier. On sync, update existing transactions if modified, soft-delete if removed by Plaid.

### FR-4: Balance Sync (Backend)

Use Plaid's `/accounts/balance/get` for real-time balance retrieval.

**Trigger:** After each transaction sync, pull current balances.

**Balance mapping:**

| Plaid Field | Spearmint Field | Notes |
|-------------|-----------------|-------|
| `balances.current` | `current_balance` | Account's current balance |
| `balances.available` | (new field) | Available balance (after holds) |
| `balances.limit` | (new field) | Credit limit for credit cards |

**Balance snapshots:** Create an `AccountBalance` record after each sync with `balance_type = 'plaid'` to build balance history automatically.

### FR-5: Investment Holdings Sync (Backend)

Use Plaid's `/investments/holdings/get` for investment account data.

**Holdings mapping:**

| Plaid Field | Spearmint Field | Notes |
|-------------|-----------------|-------|
| `security.ticker_symbol` | `symbol` | Stock/fund ticker |
| `security.name` | `description` | Security name |
| `quantity` | `quantity` | Number of shares |
| `cost_basis` | `cost_basis` | Total cost basis |
| `institution_value` | `current_value` | Current market value |
| `institution_price` | `current_price` | Per-share price |

**Sync frequency:** Daily, triggered after transaction sync.

### FR-6: Account Creation from Plaid (Backend)

When a user links accounts via Plaid, automatically create Spearmint `Account` records.

**Account mapping:**

| Plaid Field | Spearmint Field | Notes |
|-------------|-----------------|-------|
| `name` | `account_name` | Account nickname |
| `type` + `subtype` | `account_type` | Map Plaid types to Spearmint's 9 types |
| `mask` | `account_number_last4` | Last 4 digits |
| `official_name` | `notes` | Full account name from institution |
| Institution name | `institution_name` | From Plaid metadata |

**Plaid-to-Spearmint account type mapping:**

| Plaid Type | Plaid Subtype | Spearmint Type |
|------------|---------------|----------------|
| depository | checking | checking |
| depository | savings | savings |
| credit | credit card | credit_card |
| loan | student, auto, mortgage, personal | loan |
| investment | brokerage | brokerage |
| investment | 401k | 401k |
| investment | ira, roth, sep ira | ira |
| investment | (other) | investment |
| other | * | other |

### FR-7: Error Handling & Re-authentication

Handle Plaid connection errors gracefully.

| Error Scenario | User Experience | Backend Action |
|----------------|-----------------|----------------|
| `ITEM_LOGIN_REQUIRED` | Banner: "Your [Bank] connection needs attention" + "Reconnect" button | Set `error_code` on PlaidItem, stop syncing |
| `INSTITUTION_DOWN` | No user action needed | Retry on next webhook |
| `RATE_LIMIT_EXCEEDED` | No user action needed | Exponential backoff |
| `TRANSACTIONS_SYNC_MUTATION_DURING_PAGINATION` | No user action needed | Restart sync from last cursor |

### FR-8: Plaid Webhook Handler (Backend)

Register and handle Plaid webhooks for real-time data updates.

| Webhook Type | Code | Action |
|-------------|------|--------|
| `TRANSACTIONS` | `SYNC_UPDATES_AVAILABLE` | Trigger `/transactions/sync` for the item |
| `TRANSACTIONS` | `INITIAL_UPDATE` | Mark initial sync complete |
| `ITEM` | `ERROR` | Update PlaidItem error status, notify user |
| `ITEM` | `PENDING_EXPIRATION` | Prompt user to re-authenticate |
| `HOLDINGS` | `DEFAULT_UPDATE` | Trigger `/investments/holdings/get` |

**Security:** Verify webhook signatures using Plaid's webhook verification endpoint.

---

## Non-Functional Requirements

### NFR-1: Security

- Access tokens encrypted at rest using AES-256
- Access tokens never exposed to the frontend or logged
- Webhook signature verification on all incoming Plaid webhooks
- Plaid Link handles all credential entry — Spearmint never sees bank passwords
- SOC 2 Type II compliance maintained (Plaid is SOC 2 certified)
- User can revoke access at any time (unlink removes Plaid connection)

### NFR-2: Performance

- Initial transaction sync (2 years): complete within 5 minutes
- Incremental sync: complete within 30 seconds
- Balance refresh: <5 seconds
- Webhook processing: <60 seconds from receipt to data available

### NFR-3: Reliability

- Retry failed syncs with exponential backoff (max 3 retries)
- Graceful degradation: if Plaid is down, app continues working with last-synced data
- Sync status visible to user: "Last synced: 2 hours ago"

### NFR-4: Data Privacy

- Clear consent flow: users understand what data Plaid accesses
- Data deletion: when user unlinks, offer option to delete imported data or keep it
- Privacy policy updated to reflect Plaid data sharing

### NFR-5: Cost Management

- Monitor per-link costs via Plaid Dashboard
- Alert if monthly Plaid costs exceed budget threshold
- Consider caching balance requests to reduce API calls

---

## Technical Architecture

### New Database Models

```python
class PlaidItem(Base):
    """Represents a Plaid connection (one per institution per user)."""
    __tablename__ = 'plaid_items'

    id = Column(Integer, primary_key=True)
    item_id = Column(String(100), unique=True, nullable=False)  # Plaid's item ID
    access_token_encrypted = Column(LargeBinary, nullable=False)  # AES-256 encrypted
    institution_id = Column(String(50))
    institution_name = Column(String(200))
    cursor = Column(Text)  # For /transactions/sync pagination
    consent_expiration = Column(DateTime)
    error_code = Column(String(100))
    error_message = Column(Text)
    last_synced_at = Column(DateTime)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    # Relationships
    accounts = relationship('Account', back_populates='plaid_item')


# Add to existing Account model:
# plaid_item_id = Column(Integer, ForeignKey('plaid_items.id'), nullable=True)
# plaid_account_id = Column(String(100))  # Plaid's account ID within the item
# plaid_item = relationship('PlaidItem', back_populates='accounts')
```

### New API Routes

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/plaid/link-token` | Create a Plaid Link token |
| POST | `/api/plaid/exchange-token` | Exchange public token for access token |
| POST | `/api/plaid/webhook` | Receive Plaid webhooks |
| POST | `/api/plaid/accounts/{id}/sync` | Manually trigger sync for an account |
| DELETE | `/api/plaid/items/{id}` | Unlink a Plaid connection |
| GET | `/api/plaid/items` | List active Plaid connections |
| POST | `/api/plaid/items/{id}/update-link` | Get link token for re-authentication |

### Data Flow

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  User's Bank │────►│    Plaid     │────►│  Spearmint   │
│  Accounts    │     │  Platform    │     │  Backend     │
└──────────────┘     └──────┬───────┘     └──────┬───────┘
                            │                     │
                   ┌────────┴────────┐           │
                   │                 │           │
              Plaid Link        Webhooks    Store & Process
              (Frontend)     (Background)       │
                   │                 │           │
                   ▼                 ▼           ▼
              ┌──────────────────────────────────────┐
              │           Spearmint Database          │
              │  PlaidItems → Accounts → Transactions │
              │              → Balances → Holdings    │
              └──────────────────────────────────────┘
```

### Frontend Changes

| Component | Change |
|-----------|--------|
| `AccountsPage.tsx` | Add "Link Account" button alongside "Add Account" |
| `AddAccountDialog.tsx` | Add tab/option: "Link with Plaid" vs "Add Manually" |
| `AccountDetailsDialog.tsx` | Show sync status, last synced time, reconnect button for linked accounts |
| New: `PlaidLink.tsx` | Wrapper component for `@plaid/react-plaid-link` SDK |
| `AccountCard` | Badge indicating "linked" vs "manual" account |

---

## Implementation Phases

### Phase 1: Core Transaction Sync (MVP)

**Scope:** Account linking, transaction sync, balance sync
**Timeline:** 3-4 weeks
**Dependencies:** Plaid developer account, webhook endpoint (public URL or tunnel)

Deliverables:
- [ ] Plaid developer account setup and API keys
- [ ] `PlaidItem` database model and migrations
- [ ] Add `plaid_item_id` and `plaid_account_id` to Account model
- [ ] Backend: `/plaid/link-token`, `/plaid/exchange-token` endpoints
- [ ] Backend: Transaction sync service using `/transactions/sync`
- [ ] Backend: Plaid webhook handler with signature verification
- [ ] Backend: Plaid category → Spearmint category mapping
- [ ] Frontend: Plaid Link integration in AddAccountDialog
- [ ] Frontend: Sync status display on account cards
- [ ] Encrypted access token storage

### Phase 2: Investment Holdings & Enhanced Balances

**Scope:** Investment data, balance history, portfolio sync
**Timeline:** 2 weeks
**Dependencies:** Phase 1 complete

Deliverables:
- [ ] Backend: Investment holdings sync via `/investments/holdings/get`
- [ ] Backend: Automatic daily balance snapshots from Plaid
- [ ] Frontend: Auto-populated portfolio tab for linked investment accounts
- [ ] Frontend: Real-time balance display on account cards

### Phase 3: Error Handling & Polish

**Scope:** Re-authentication, error recovery, connection management
**Timeline:** 2 weeks
**Dependencies:** Phase 2 complete

Deliverables:
- [ ] Backend: Error detection and PlaidItem status management
- [ ] Frontend: Re-authentication banner and flow
- [ ] Frontend: "Manage Connections" view showing all linked institutions
- [ ] Frontend: Unlink flow with data retention options
- [ ] Webhook retry logic with exponential backoff
- [ ] Monitoring and alerting for sync failures

### Phase 4: Transfer Detection & Categorization (Post-MVP)

**Scope:** Cross-account transfer detection, category learning
**Timeline:** 2 weeks
**Dependencies:** Phase 3 complete, multiple linked accounts in use

Deliverables:
- [ ] Backend: Detect transfers between linked accounts (matching amounts, dates)
- [ ] Backend: Seed classification rules from Plaid's merchant categorization
- [ ] Frontend: Transfer confirmation UI
- [ ] Analytics: Plaid cost tracking dashboard

---

## Open Questions

1. **Plaid pricing tier:** Which Plaid plan should we start with? Pay-as-you-go is cheapest for <500 users, Growth tier ($100/month) at ~100+ links.

2. **Webhook infrastructure:** Do we need a public URL for webhooks in production, or can we use Plaid's sandbox webhook testing for development? Consider using a webhook relay service for self-hosted deployments.

3. **Multi-user support:** The current Spearmint architecture appears single-user. If we add Plaid, do we need to scope access tokens per user? For self-hosted single-user, one set of tokens may suffice.

4. **Existing Tiller PRD:** Should the Tiller integration (via Google Sheets) still be pursued, or does direct Plaid integration supersede it? Recommendation: Plaid supersedes Tiller for most users, but Tiller remains useful for institutions Plaid doesn't support.

5. **KI-001 prerequisite:** Transaction `account_id` linking (KI-001) should be resolved before Phase 1 begins, as Plaid transactions must be associated with specific accounts.

---

## References

- [Plaid API Documentation](https://plaid.com/docs/)
- [Plaid React SDK (`react-plaid-link`)](https://github.com/plaid/react-plaid-link)
- [Plaid Python SDK](https://github.com/plaid/plaid-python)
- [Plaid Transactions Sync Guide](https://plaid.com/docs/transactions/sync/)
- [Plaid Webhooks Guide](https://plaid.com/docs/transactions/webhooks/)
- `product/TILLER_INTEGRATION_PRD.md` — Related integration PRD (Tiller/spreadsheet approach)
- `product/feature-planning/budget-advisor-agent.md` — Budget Advisor PRD (depends on transaction data quality)
- `core-api/src/financial_analysis/services/import_service.py` — Current import implementation
- `core-api/src/financial_analysis/database/models.py` — Data models

---

## Appendix A: Plaid vs Yodlee Evaluation

### Decision: Plaid (Recommended)

| Criterion | Plaid | Yodlee | Winner |
|-----------|-------|--------|--------|
| **Pricing (small scale)** | $0.50-$2.00/link, no minimums | $8K-$15K/month at 5K users | Plaid |
| **Developer experience** | Official Python + React SDKs, excellent docs, 1-2 week integration | Java SDK only, 4-8 week integration, enterprise sales required | Plaid |
| **Institution coverage** | 12,000+ (~95% US) | 17,000+ (broader international) | Yodlee |
| **Transaction history** | Up to 2 years | 90 days default, 1 year extended | Plaid |
| **Transaction categorization** | 89% accuracy, AI-enhanced (2025) | 92% accuracy | Tie |
| **Investment data** | Holdings, cost basis, current value | Richer subtypes (ROTH_SIMPLE_IRA, etc.) | Yodlee |
| **PFM track record** | YNAB, Copilot, Monarch use Plaid | More enterprise/institutional focus | Plaid |
| **Self-serve signup** | Yes, instant sandbox access | No, enterprise sales process required | Plaid |
| **Sandbox quality** | Full sandbox with test institutions | Sandbox/prod inconsistencies reported | Plaid |
| **Compliance** | SOC 2 Type II, ISO 27001, ISO 27701 | SOC 2 Type II | Plaid |

**Bottom line:** Plaid is the clear choice for Spearmint's scale and self-hosted architecture. Yodlee's advantages (broader coverage, richer investment subtypes) don't justify the 10-30x cost premium and significantly longer integration cycle. If Spearmint grows to enterprise scale with international requirements, Yodlee could be evaluated as a secondary aggregator.

---

## Appendix B: Revision History

| Date | Author | Changes |
|------|--------|---------|
| 2026-03-15 | Accounts Team | Initial draft |
