# Your First Import

This guide walks you through importing your first bank file into Spearmint.

## Supported File Formats

Spearmint accepts:
- **Excel files** (.xlsx, .xls)
- **CSV files** (.csv)

Most banks offer transaction exports in one of these formats. Check your bank's website for "Download Transactions" or "Export" options.

## Step 1: Get Your Bank Export

1. Log into your bank's website
2. Navigate to your account's transaction history
3. Look for "Download," "Export," or "Download Transactions"
4. Choose CSV or Excel format
5. Select your desired date range
6. Download the file

### Common Bank Export Locations

| Bank | Where to Find Export |
|------|---------------------|
| Chase | Statements & Documents → Download Account Activity |
| Bank of America | Statements & Documents → Download Transactions |
| Wells Fargo | Account Activity → Download |
| Capital One | Download Transactions (top right of activity) |
| Discover | Statements → Download Activity |

## Step 2: Import into Spearmint

1. Open Spearmint in your browser (`http://localhost:5173`)
2. Navigate to **Import** in the sidebar
3. **Drag and drop** your file onto the import area, or click to browse
4. Spearmint will analyze your file

## Step 3: Map Your Columns

Different banks use different column names. Spearmint needs to know which columns contain:

| Spearmint Field | What It Means | Example Bank Headers |
|-----------------|---------------|---------------------|
| **Date** | Transaction date | "Posting Date", "Trans Date", "Date" |
| **Amount** | Transaction amount | "Amount", "Value", "Debit/Credit" |
| **Description** | Transaction description | "Description", "Details", "Memo" |
| **Category** | (Optional) Bank's category | "Category", "Type" |

### First-Time Mapping

When Spearmint sees a new file format:

1. It displays the detected columns from your file
2. You drag each column to its corresponding Spearmint field
3. You can specify:
   - **Date format** (e.g., MM/DD/YYYY, YYYY-MM-DD)
   - **Skip rows** (if your file has header rows to ignore)

### Save as Import Profile

After mapping, you can save this configuration as an **Import Profile**:

1. Give it a name (e.g., "Chase Credit Card", "Checking Account")
2. Optionally link it to an account in Spearmint
3. Click **Save Profile**

Next time you import from the same bank, Spearmint will recognize the format and suggest your saved profile — no re-mapping needed!

## Step 4: Review and Confirm

Before importing, Spearmint shows you:

- **Preview** of the first few transactions
- **Total count** of transactions found
- **Date range** detected
- **Any issues** (missing required fields, parsing errors)

Review the preview to ensure the data looks correct, then click **Import**.

## Step 5: View Your Transactions

After import, navigate to **Transactions** to see your data:

- Transactions are sorted by date (newest first)
- Use filters to narrow by date range, amount, or category
- Click any transaction to see details or edit

## What Happens Next?

Once imported, Spearmint automatically:

1. **Detects patterns** — Identifies recurring transactions
2. **Suggests categories** — Based on description matching
3. **Finds relationships** — Detects transfers between accounts
4. **Calculates metrics** — Updates your cash flow analysis

## Tips for Best Results

### Import All Accounts

For accurate transfer detection and cash flow analysis, import transactions from all your accounts:
- Checking accounts
- Savings accounts
- Credit cards
- Investment accounts (for cash transactions)

### Use Consistent Date Ranges

When importing multiple accounts, use the same date range to ensure transfers are matched correctly.

### Re-import Safely

Spearmint handles duplicate detection. If you accidentally import the same file twice, duplicates are identified and can be managed.

---

**Next Steps:**

- [Set up your accounts](../concepts/accounts.md)
- [Learn about classifications](../concepts/classifications.md)
- [View your cash flow](../features/cash-flow-analysis.md)

