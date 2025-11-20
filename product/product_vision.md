Think Big – $pearmint

Date: November 20, 2025
Status: Draft
Owner: Product Management

Purpose

This document presents the long-term vision for $pearmint, a financial platform that evolves the concept of personal finance from simple tracking to professional-grade management. It addresses a gap in the market for a tool that combines the ease of consumer apps with the analytical rigor of business software, provided as a free, self-hosted engine.

Background

For over a decade, Mint.com introduced millions to the value of automated financial tracking. Its closure marked the end of an era, but also highlighted a limitation in the consumer fintech market: most tools are designed to track spending, not to manage wealth.

Current alternatives, while visually polished, often lack the accounting depth required for complex modern lives. A $20,000 home renovation is fundamentally different from a grocery bill, yet most apps treat them identical—as "expenses" that blow the monthly budget. Users who manage rental properties, split custody, or irregular income streams need more than a list of transactions; they need a tool that understands cash flow, capital investments, and forecasting. $pearmint bridges this gap.

What is $pearmint?

$pearmint is a "Personal CFO" that runs on your infrastructure. It is an open-source financial engine that transforms raw transaction data into professional-grade accounting intelligence—offering features like Capital Expenditure tracking, true burn rate analysis, and confidence-based forecasting.

By running locally on the user's hardware (via Docker), $pearmint delivers distinct advantages:

Professional Depth: It treats the household like a business entity, separating operating costs from investments.

Zero Cost: By utilizing the user's own hardware, it eliminates the need for monthly subscription fees.

Unlimited Horizon: Users can store decades of high-fidelity history and attachments without hitting cloud storage limits.

Press Release (Future State)

FOR IMMEDIATE RELEASE

$pearmint Launches: Business-Class Finance for the Household

VENTNOR CITY, NJ – January 15, 2026 – Today, the open-source community announces the release of $pearmint, a new platform that brings the sophistication of business accounting to personal finance, completely free of charge.

For years, consumers have had to choose between simple expense trackers or complex spreadsheets to manage their money. $pearmint offers a third path: a powerful, automated financial engine that runs locally, providing the depth of professional software with the usability of a consumer app.

"We believe managing a household's finances requires the same level of clarity as managing a business," said the Lead Maintainer. "With $pearmint, we are giving families the tools to distinguish between the cost of living and the cost of building wealth."

$pearmint introduces "Business-Grade Personal Finance." Unlike traditional apps, $pearmint separates "Operational Costs" (groceries, utilities) from "Capital Expenditures" (remodels, vehicles), giving families a true view of their monthly operating burn. It also introduces "Confidence Modeling," allowing users to forecast their financial runway based on variable income scenarios.

"I loved the automation of Mint, but I needed more control," said Sarah Jenkins, a beta user and Family CFO. "$pearmint respects the complexity of my life. It handles reimbursements, renovations, and shared expenses effortlessly, and I love that I own the data myself."

$pearmint is available today as a self-hosted Docker container, bringing professional financial clarity to anyone with a computer.

Walkthrough: The User Journey

Scene 1: Installation (The "Appliance" Setup)

Sarah, a technically savvy user looking for a robust financial tool, visits the $pearmint GitHub repository.
She copies a single docker-compose.yml file to her home server and types docker-compose up -d.
Within seconds, she has a fully functional financial analytics platform running on her own metal. No credit card required. No trial period. It is hers forever.

Scene 2: Ingestion (The Universal Adapter)

Sarah logs in to a clean, empty dashboard. A prominent card reads: "No Data Found. Drag & Drop your Bank CSV here."
She logs into Chase.com in a separate tab, downloads her "2024 Activity.csv," and drags the file onto the $pearmint dashboard.
The system analyzes the file but doesn't guess blindly.
System: "I've detected a new format. Let's map it to the $pearmint Ledger."
Action: Sarah sees the raw CSV headers on the left (e.g., "Posting Date," "Details," "Amount"). She drags them to the standard fields on the right (Date, Description, Value).
System: "Mapping saved as 'Chase Credit Card'. I will remember this for next time."
The dashboard populates instantly. The friction of manual import becomes a one-time configuration task, giving her confidence that her data is normalized correctly across all her banks.

Scene 3: The "Renovation" Moment (CapEx Separation)

Sarah navigates to the Ledger view. She sees a $15,000 charge for "Home Depot" from last month—her kitchen remodel. In previous apps, this destroyed her "Monthly Spending" graph, creating a false alarm that she was over budget.
In $pearmint, she clicks the transaction.
Action: She toggles a switch labeled "Capital Expenditure (CapEx)."
Result: The "Home Depot" charge disappears from her "Operating Expenses" chart and moves to the "Asset Investment" chart.
She looks at her "Monthly Burn Rate." It drops from $18,000 to $3,000—her actual living expenses. She sees clearly that she isn't overspending; she is investing in her asset.

Scene 4: The "Work Trip" Split (Entity Tagging)

She scrolls down to a $1,200 charge for "United Airlines." This was for a work conference that her company will reimburse.
Action: She right-clicks the transaction. She selects "Mark as Reimbursable."
Action: She tags the entity "Employer."
Result: The $1,200 charge disappears from her personal "Spending" report. It moves to a "Receivables" widget on her dashboard, creating a shadow ledger entry. She now has a clear list of money owed to her, ensuring she never forgets to file an expense report, and her personal budget remains accurate.

Scene 5: Cash Flow Analysis (The Pulse)

Sarah navigates to the Cash Flow view to check her financial health. A waterfall chart displays her month-to-date performance.
She sees a tall green bar for "Income" and a stack of red bars for "Expenses." The "Net Cash Flow" line dips negative because of the renovation.
Action: She clicks the "Exclude CapEx" filter.
Result: The chart redraws instantly. The large "Home Depot" block vanishes. The "Net Cash Flow" line jumps back into the positive.
She sees a trend line indicating her "Operating Margin" has actually improved by 15% over the last three months. She confirms that her core habits generate positive cash, giving her peace of mind despite the large renovation checks.

Scene 6: Active Budgeting (The Flexible Plan)

She switches to the Budget tab to plan her upcoming spending.
She sees a "Groceries" category bar turning yellow. She is close to her monthly limit.
She notices her "Utilities" category has $50 remaining because of mild weather.
Action: She drags that $50 surplus from "Utilities" and drops it onto "Groceries."
Result: The bars adjust instantly. Groceries turns green again.
She realizes she doesn't need to restrict her food shopping this week because she saved elsewhere. The budget reflects her choices, not just her constraints.

Scene 7: Forecasting (The Cone of Uncertainty)

Finally, Sarah goes to the Forecast tab. She is worried about her job stability.
Action: She sees a projection of her bank balance for the next 6 months.
Action: She adds a potential "Bonus" of $5,000 in December but sets the Confidence Slider to 40%.
Result: The graph splits. A solid line shows her "Safe Path" (assuming no bonus). A dotted line shows the "Optimistic Path."
She sees that even on the Safe Path, she has 4 months of runway. She closes the laptop, feeling a sense of control she hasn't felt in years.

The Strategic Opportunity

The closure of Mint.com created a diaspora of 3.6 million active users. Many of these users are technically literate professionals who are looking for a tool that respects their intelligence and data.

By launching V1 as a high-quality, self-hosted tool, we capture the "Architecture-First" influencers—the tech-savvy users who recommend tools to their friends and family. This establishes credibility and a community-driven plugin ecosystem. Once the core engine is perfected by this demanding audience, we will expand to a wider audience through a managed "Private Cloud" offering that removes the technical barrier of Docker while maintaining the platform's unique capabilities.

How Do We Get There?

We will avoid the feature-bloat trap of trying to copy every feature of legacy tools. Instead, we focus on three horizons:

Horizon 1: The Sovereign Foundation (V1)

Goal: Be the best self-hosted ledger on the market.

Focus: Flawless CSV ingestion, smart local categorization rules, and sub-100ms performance for sorting/filtering.

Constraint: No cloud dependencies. Everything runs via docker-compose.

Horizon 2: The Intelligent Analyst (V2)

Goal: Answer "What if?" questions.

Focus: Forecasting engines, confidence modeling, and scenario planning (e.g., "What if I lose my job next month?").

Differentiation: Separating CapEx from OpEx to show "True Burn," a feature no consumer app currently offers.

Horizon 3: The Private Cloud (Future)

Goal: Convenience for everyone.

Focus: A managed service where we host the instance, but the user holds the encryption keys. This competes directly with SaaS alternatives but differentiates on privacy and cost.

FAQ

Q: Why self-hosted first? isn't that a small market?
It is a focused and influential market. These users (the "Homelab" community) provide the rigorous testing and community contributions needed to build a robust engine before we scale to the mass market.

Q: Is it really free?
Yes. Because you provide the hardware (your own computer or server), there are no cloud costs for us to pass on to you. It is free software in the truest sense.

Q: Mint was automatic. Is CSV uploading too much friction?
For the mass market, yes. For the V1 target persona, it ensures accuracy and reliability without relying on third-party APIs. We will add optional automation plugins later for those who prioritize convenience over strict isolation.

Q: Can I check my budget on my phone while at the store?
Yes. The web application is responsive and works on mobile browsers. We recommend installing a private VPN (like Tailscale) on your phone to access your home server securely from anywhere. We plan to build a native mobile app in Horizon 2.

Q: How do I handle shared family finances?
You can create multiple user accounts for your household. All users access the same "Master Ledger." You can tag transactions by person (e.g., "Dad," "Mom," "Kids") to track individual spending within the shared budget.

Q: What happens if my computer crashes?
Your data lives in a standard Docker volume. You can back up the data by copying a single folder. We also provide a script to encrypt and push backups to an S3 bucket or NAS automatically.

Q: Is there a "Dark Mode"?
Yes. The interface supports light and dark themes to match your system preferences.