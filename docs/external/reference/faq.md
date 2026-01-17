# Frequently Asked Questions

## General

### What is Spearmint?

Spearmint is a self-hosted personal finance platform that brings business-grade accounting intelligence to household finances. It runs on your own hardware via Docker, giving you complete control over your financial data.

### Is Spearmint really free?

Yes. Because you provide the hardware (your own computer or home server), there are no cloud costs for us to pass on. It's free software in the truest sense.

### Why self-hosted?

Self-hosting provides:
- **Data ownership** — Your financial data stays on your hardware
- **Privacy** — No third party sees your transactions
- **No shutdowns** — No company going out of business takes your data
- **Unlimited history** — Store decades of data without hitting limits
- **No ads** — We don't monetize your attention or data

### Who is Spearmint for?

Spearmint is designed for people who:
- Want control over their financial data
- Have complex finances (investments, rentals, side income)
- Value accuracy over simplicity
- Are comfortable running Docker
- Miss Mint but want something more powerful

---

## Installation & Setup

### What do I need to run Spearmint?

- A computer or server that can run Docker
- A modern web browser
- Your bank export files (CSV or Excel)

### Can I run Spearmint on a Raspberry Pi?

Yes, with caveats. Spearmint runs on ARM architecture, but performance may be limited for large datasets. A Pi 4 with 4GB+ RAM should work for moderate use.

### Can I run Spearmint on my NAS?

Many NAS devices (Synology, QNAP) support Docker. Check your NAS documentation for Docker/container support.

### How do I access Spearmint remotely?

Spearmint runs as a web application on your local network. For secure remote access:
- Set up a VPN like Tailscale or WireGuard
- Access via VPN from anywhere
- We do not recommend exposing Spearmint directly to the internet

---

## Data & Import

### Does Spearmint connect to my bank automatically?

Currently, no. Spearmint V1 uses manual import of CSV/Excel files from your bank. This is intentional:
- Ensures data accuracy
- Avoids third-party API dependencies
- Respects privacy

Automatic sync is on the roadmap for future versions.

### How do I get data from my bank?

Most banks offer CSV or Excel export:
1. Log into your bank's website
2. Go to transaction history
3. Look for "Download" or "Export"
4. Select CSV or Excel format
5. Import into Spearmint

### Can I import from Mint?

If you exported your Mint data before it shut down, yes! Import your Mint CSV and map the columns to Spearmint's format.

### How often should I import?

Weekly or monthly works well. Regular imports help you:
- Stay on top of your finances
- Catch issues early
- Build good financial habits

---

## Features

### What's the difference between Categories and Classifications?

- **Categories** answer "What kind of spending?" (groceries, rent, entertainment)
- **Classifications** answer "How should this affect calculations?" (regular expense, transfer, CapEx)

Both are important. Categories organize; classifications calculate.

### What is CapEx?

Capital Expenses (CapEx) are one-time investments in long-term assets — renovations, vehicles, major equipment. Spearmint separates these from Operating Expenses (OpEx) so your monthly spending view isn't distorted.

### How does transfer detection work?

Spearmint looks for matching transactions:
- Same amount, opposite signs
- Within a few days
- Between accounts you own

Detected pairs are linked and excluded from income/expense totals.

### Can I use Spearmint for a business?

Spearmint is designed for personal/household finances, but works well for:
- Freelancers separating business and personal
- Small sole proprietorships
- Side hustles

For complex business accounting, consider dedicated business software.

---

## Mobile & Access

### Is there a mobile app?

Not yet. Spearmint is a responsive web application that works in mobile browsers. Native mobile apps are planned for future releases.

### Can I check my finances on my phone?

Yes! Access the web app via mobile browser:
1. When on your home network, just browse to Spearmint's URL
2. When away, use a VPN to access your home network securely

---

## Data Safety

### What happens if my computer crashes?

Your data is stored in a Docker volume (a folder on your system). To protect it:
- Back up the data folder regularly
- Use your existing backup solution
- Spearmint can provide scripts for automated backup

### Can I migrate to a new computer?

Yes! Copy the Docker volume to your new machine and start Spearmint. Your data comes with it.

### Is my data encrypted?

Data is stored locally in SQLite format. It's not encrypted at rest by default. For encryption:
- Use full-disk encryption on your server
- Store the Docker volume on an encrypted drive

---

## Troubleshooting

### My balances don't match my bank statements

This usually means:
- Missing transactions (need to import more)
- Duplicate transactions (imported same file twice)
- Wrong date range imported

Use the Reconciliation Report to identify discrepancies.

### Transfers aren't being detected

Check that:
- Both accounts are imported
- Transactions are within 7 days of each other
- Amounts match exactly (or very closely)

You can also link transfers manually.

### A category rule isn't matching

Rules are case-sensitive and use pattern matching. Check:
- The pattern exactly matches part of the description
- Priority is set correctly (higher priority wins)
- The rule is enabled

---

## Future Plans

### Will Spearmint add automatic bank sync?

It's on the roadmap. We're exploring privacy-preserving approaches that maintain the self-hosted philosophy.

### What about budgeting features?

Budget tracking with category limits is planned for a future release.

### Will there be a mobile app?

Native mobile apps are planned for future development.

---

**Still have questions?**
- Check our [documentation](../README.md)
- Open an issue on [GitHub](https://github.com/spearmint-finance/spearmint/issues)

