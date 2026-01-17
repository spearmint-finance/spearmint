# Import Profiles

Import Profiles save your column mapping configurations so you don't have to re-map every time you import from the same bank.

## The Problem

Every bank exports transactions differently:

| Bank | Date Column | Amount Column | Description Column |
|------|-------------|---------------|-------------------|
| Chase | "Posting Date" | "Amount" | "Description" |
| Bank of America | "Date" | "Amount" | "Payee" |
| Capital One | "Transaction Date" | "Debit/Credit" | "Description" |
| Wells Fargo | "Date" | "Amount" | "Description" |

Without Import Profiles, you'd manually map columns every single time.

## How Import Profiles Work

### First Import from a New Bank

1. Upload your bank's CSV/Excel file
2. Spearmint detects the columns
3. You map each column to Spearmint's fields:
   - Date → "Posting Date"
   - Amount → "Amount"
   - Description → "Description"
4. Configure options:
   - Date format (e.g., MM/DD/YYYY)
   - Rows to skip (for header rows)
5. **Save as Import Profile**

### Subsequent Imports

1. Upload your file
2. Spearmint suggests matching profiles based on column headers
3. Select your saved profile
4. Import — no mapping needed!

## Creating an Import Profile

### From the Import Page

1. Navigate to **Import**
2. Upload your file
3. Map the columns as needed
4. Click **Save as Profile**
5. Enter:
   - **Name** — e.g., "Chase Credit Card"
   - **Account** (optional) — Link to a Spearmint account
6. Save

### From Profile Management

1. Navigate to **Settings → Import Profiles**
2. Click **Create Profile**
3. Configure:
   - Name
   - Column mappings
   - Date format
   - Skip rows
   - Linked account
4. Save

## Profile Settings

| Setting | Description | Example |
|---------|-------------|---------|
| **Name** | Friendly name for the profile | "Chase Sapphire Card" |
| **Column Mappings** | Which CSV columns map to which fields | `{"date": "Posting Date", "amount": "Amount"}` |
| **Date Format** | How dates are formatted | "MM/DD/YYYY", "YYYY-MM-DD" |
| **Skip Rows** | Number of header rows to skip | 1, 2 |
| **Account** | Spearmint account to associate | "Chase Credit Card" |
| **Active** | Whether profile appears in suggestions | true/false |

## Profile Suggestions

When you upload a file, Spearmint analyzes its columns and suggests matching profiles:

```
Detected columns: Posting Date, Amount, Description, Type, Category

Matching profiles:
  ✓ Chase Credit Card (95% match)
  ○ Chase Checking (80% match)
  ○ Bank of America (40% match)
```

The match score is based on how many columns in the file match the profile's expected columns.

## Managing Profiles

### View All Profiles

Navigate to **Settings → Import Profiles** to see all saved profiles.

### Edit a Profile

Click any profile to modify:
- Update column mappings
- Change date format
- Link to a different account
- Rename

### Deactivate a Profile

If you close a bank account, you can deactivate its profile rather than delete it:
- Deactivated profiles don't appear in suggestions
- Historical imports still reference the profile
- You can reactivate anytime

### Delete a Profile

Permanently remove a profile you no longer need.

## Tips for Effective Profiles

### One Profile Per Account Format

Create separate profiles even for the same bank if formats differ:
- "Chase Credit Card"
- "Chase Checking" (different columns)

### Use Descriptive Names

Include the bank and account type:
- ✅ "Ally Savings Account"
- ❌ "Savings" (too generic)

### Link to Accounts

Linking a profile to an account means:
- Imported transactions auto-assign to that account
- Easier filtering and reporting
- Transfer detection works better

### Keep Date Formats Accurate

Common formats:
- `MM/DD/YYYY` — 01/15/2025
- `YYYY-MM-DD` — 2025-01-15
- `DD/MM/YYYY` — 15/01/2025 (common outside US)

Wrong date format = wrong transaction dates = confusion!

---

**Related:**
- [Your First Import](../getting-started/first-import.md) — Getting started with imports
- [Accounts](../concepts/accounts.md) — Setting up accounts to link

