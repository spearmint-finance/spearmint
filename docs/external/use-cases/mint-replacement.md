# Replacing Mint.com with Spearmint

If you're one of the millions who relied on Mint.com before it shut down, Spearmint offers a powerful alternative with capabilities that go beyond what Mint provided.

## What You Loved About Mint

Mint was revolutionary for its time:
- ✅ Automatic bank connections
- ✅ Transaction categorization
- ✅ Budget tracking
- ✅ Bill reminders
- ✅ Free to use

## What Mint Lacked

But Mint had limitations:
- ❌ No capital expense separation
- ❌ Poor handling of transfers
- ❌ Limited forecasting
- ❌ Data owned by Intuit
- ❌ Ads and upselling
- ❌ Limited history access

## How Spearmint Compares

| Feature | Mint | Spearmint |
|---------|------|-----------|
| **Auto-sync with banks** | ✅ Yes | 🔜 Coming (manual import for now) |
| **Transaction categorization** | ✅ Basic | ✅ Advanced with rules |
| **Budget tracking** | ✅ Yes | 🔜 Coming |
| **Transfer detection** | ⚠️ Inconsistent | ✅ Automatic |
| **CapEx separation** | ❌ No | ✅ Yes |
| **Forecasting** | ⚠️ Basic | ✅ Multiple methods with confidence |
| **Data ownership** | ❌ Their servers | ✅ Your hardware |
| **Cost** | "Free" (with ads) | ✅ Actually free |
| **History limits** | 90 days - 2 years | ✅ Unlimited |
| **Offline access** | ❌ No | ✅ Yes (local) |

## Migrating from Mint

### Step 1: Export Your Mint Data

Before Mint shut down, you hopefully exported your data. If you did:
1. Locate your Mint CSV export
2. This file contains your transaction history

### Step 2: Install Spearmint

Follow the [installation guide](../getting-started/installation.md):
```bash
docker-compose up -d
```

### Step 3: Import Your History

1. Navigate to **Import**
2. Upload your Mint CSV
3. Map the columns (Mint format):
   - Date → "Date"
   - Description → "Description" 
   - Original Description → (optional)
   - Amount → "Amount"
   - Category → "Category"
   - Account Name → "Account"
4. Save as "Mint Export" profile
5. Import

### Step 4: Set Up Your Accounts

Create accounts in Spearmint matching your real accounts:
- Checking
- Savings
- Credit cards
- Investment accounts

### Step 5: Import Current Data

Going forward, export from each bank and import into Spearmint:
1. Download CSV/Excel from your bank
2. Create an import profile for that bank's format
3. Import regularly (weekly or monthly)

## What You'll Gain

### Accurate Spending Analysis

Mint often miscounted transfers and credit card payments. Spearmint's [classification system](../concepts/classifications.md) ensures accurate totals.

### Capital Expense Tracking

That $15,000 renovation no longer destroys your monthly budget view. Mark it as [CapEx](../concepts/capex-vs-opex.md) and see your true operating expenses.

### Better Forecasting

Mint's "trends" were basic. Spearmint's [forecasting](../features/forecasting.md) uses multiple statistical methods with confidence intervals.

### Your Data, Forever

No company shutting down takes your history. Your data lives on your hardware, backed up how you choose, accessible forever.

### No Ads, No Upselling

Spearmint doesn't sell your data or push credit cards at you. It's a tool, not a marketing platform.

## What You'll Miss (For Now)

### Automatic Bank Sync

Currently, Spearmint requires manual CSV/Excel imports. This is intentional for V1:
- Ensures data accuracy
- Avoids third-party API dependencies
- Respects your privacy

Automatic sync is on the roadmap for future versions.

### Mobile App

Spearmint is currently web-based. On mobile:
- Access via browser (responsive design)
- Use VPN like Tailscale for secure remote access

Native mobile apps are planned for future releases.

## Tips for Mint Users

### Start Fresh, Then Add History

1. First, get comfortable with current data
2. Then import historical Mint data
3. This helps you learn the system

### Embrace Manual Import

Weekly imports take 5 minutes and ensure you review your finances regularly. Many users find this beneficial.

### Explore Classifications

This is Spearmint's superpower. Take time to understand how [classifications](../concepts/classifications.md) give you accurate numbers.

---

**Next Steps:**
- [Installation](../getting-started/installation.md)
- [First Import](../getting-started/first-import.md)
- [Understanding Classifications](../concepts/classifications.md)

