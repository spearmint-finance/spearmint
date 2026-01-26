"""
Demo transaction data seeder for showcasing application features.

Generates 12 months of realistic financial transactions including:
- Multiple income sources (salary, freelance, dividends, refunds)
- Varied expense categories (rent, groceries, utilities, dining, etc.)
- Classification edge cases (transfers, CC payments, reimbursements)
- Data quality test cases (miscategorized items, outliers)

Usage:
    # Standalone
    python -m src.financial_analysis.database.seed_demo_data

    # With reset (clear existing demo data first)
    python -m src.financial_analysis.database.seed_demo_data --reset

    # Via init_db
    python -m src.financial_analysis.database.init_db --reset --with-demo-data
"""

import argparse
import random
from datetime import date, timedelta
from decimal import Decimal
from typing import Optional

from sqlalchemy.orm import Session

from .base import SessionLocal
from .models import Account, Category, Transaction, TransactionClassification


# Constants
DEMO_MONTHS = 12
DEMO_MARKER = "[DEMO]"  # Prefix for demo transaction descriptions
RANDOM_SEED = 42  # For reproducible demo data


# =============================================================================
# Demo Categories
# =============================================================================

DEMO_CATEGORIES = [
    # Income categories
    {"category_name": "Salary", "category_type": "Income", "description": "Employment income"},
    {"category_name": "Freelance Income", "category_type": "Income", "description": "Contract and freelance work"},
    {"category_name": "Dividends", "category_type": "Income", "description": "Investment dividends"},
    {"category_name": "Interest", "category_type": "Income", "description": "Bank interest income"},
    {"category_name": "Refunds", "category_type": "Income", "description": "Purchase refunds and returns"},
    {"category_name": "Reimbursements", "category_type": "Income", "description": "Expense reimbursements"},

    # Expense categories
    {"category_name": "Rent/Mortgage", "category_type": "Expense", "description": "Housing payment", "is_fixed_obligation": True},
    {"category_name": "Utilities", "category_type": "Expense", "description": "Electric, gas, water, internet", "is_fixed_obligation": True},
    {"category_name": "Groceries", "category_type": "Expense", "description": "Food and household supplies"},
    {"category_name": "Dining & Restaurants", "category_type": "Expense", "description": "Eating out and food delivery"},
    {"category_name": "Transportation", "category_type": "Expense", "description": "Gas, transit, rideshare"},
    {"category_name": "Subscriptions", "category_type": "Expense", "description": "Streaming, software, memberships", "is_fixed_obligation": True},
    {"category_name": "Shopping", "category_type": "Expense", "description": "General retail purchases"},
    {"category_name": "Healthcare", "category_type": "Expense", "description": "Medical, dental, pharmacy"},
    {"category_name": "Entertainment", "category_type": "Expense", "description": "Movies, games, events"},
    {"category_name": "Insurance", "category_type": "Expense", "description": "Auto, health, life insurance", "is_fixed_obligation": True},
    {"category_name": "Personal Care", "category_type": "Expense", "description": "Haircuts, gym, wellness"},

    # Transfer categories
    {"category_name": "Transfers", "category_type": "Both", "description": "Internal account transfers", "is_transfer_category": True},
    {"category_name": "Credit Card Payment", "category_type": "Both", "description": "Credit card bill payments", "is_transfer_category": True},

    # Capital/Investment
    {"category_name": "Investments", "category_type": "Expense", "description": "Stock and fund purchases"},

    # For data quality testing - miscategorized items
    {"category_name": "Uncategorized", "category_type": "Both", "description": "Needs categorization"},
]


# =============================================================================
# Merchant/Description Templates
# =============================================================================

SALARY_EMPLOYERS = [
    "Acme Corporation",
    "TechStart Inc",
    "Global Industries",
]

FREELANCE_CLIENTS = [
    "Client Project - Web Design",
    "Consulting Services - Q{quarter}",
    "Contract Work - Development",
    "Freelance - Marketing Campaign",
]

GROCERY_MERCHANTS = [
    "Whole Foods Market",
    "Trader Joe's",
    "Safeway",
    "Costco",
    "Target",
    "Kroger",
]

DINING_MERCHANTS = [
    "Chipotle Mexican Grill",
    "Starbucks",
    "Panera Bread",
    "Local Restaurant",
    "Domino's Pizza",
    "DoorDash",
    "Uber Eats",
    "Thai Kitchen",
    "Sushi Palace",
    "Italian Bistro",
]

TRANSPORTATION_MERCHANTS = [
    "Shell Gas Station",
    "Chevron",
    "Uber",
    "Lyft",
    "BART",
    "Parking Garage",
]

SUBSCRIPTION_ITEMS = [
    ("Netflix", Decimal("15.99")),
    ("Spotify Premium", Decimal("10.99")),
    ("iCloud Storage", Decimal("2.99")),
    ("Amazon Prime", Decimal("14.99")),
    ("YouTube Premium", Decimal("13.99")),
    ("Adobe Creative Cloud", Decimal("54.99")),
    ("Gym Membership", Decimal("49.99")),
    ("News Subscription", Decimal("9.99")),
]

SHOPPING_MERCHANTS = [
    "Amazon",
    "Target",
    "Best Buy",
    "Home Depot",
    "IKEA",
    "Walmart",
    "Nordstrom",
]

HEALTHCARE_MERCHANTS = [
    "CVS Pharmacy",
    "Walgreens",
    "Kaiser Permanente",
    "Dental Office",
    "Eye Care Center",
]

ENTERTAINMENT_MERCHANTS = [
    "AMC Theaters",
    "Steam Games",
    "Concert Tickets",
    "Sporting Event",
    "Museum Admission",
]

UTILITY_COMPANIES = [
    ("PG&E Electric", Decimal("80"), Decimal("180")),
    ("Comcast Internet", Decimal("79.99"), Decimal("89.99")),
    ("Water District", Decimal("40"), Decimal("80")),
    ("Gas Company", Decimal("30"), Decimal("120")),
]


# =============================================================================
# Bank Accounts (for source field)
# =============================================================================

# Primary checking account - used for rent, utilities, auto-pay
PRIMARY_CHECKING = "Chase Checking"

# Credit cards - used for most discretionary spending
CREDIT_CARDS = [
    "Chase Sapphire",
    "Amex Gold",
    "Citi Double Cash",
]

# Debit card transactions come from checking
DEBIT_ACCOUNT = "Chase Checking"

# HSA account for healthcare
HSA_ACCOUNT = "Fidelity HSA"

# Accounts used for transfers
SAVINGS_ACCOUNT = "Marcus Savings"


# =============================================================================
# Demo Account Definitions
# =============================================================================

DEMO_ACCOUNTS = [
    {
        "account_name": "Chase Checking",
        "account_type": "checking",
        "institution_name": "Chase Bank",
        "account_number_last4": "4521",
        "has_cash_component": True,
        "opening_balance": Decimal("5000.00"),
        "notes": f"{DEMO_MARKER} Primary checking account",
    },
    {
        "account_name": "Marcus Savings",
        "account_type": "savings",
        "institution_name": "Marcus by Goldman Sachs",
        "account_number_last4": "8834",
        "has_cash_component": True,
        "opening_balance": Decimal("15000.00"),
        "notes": f"{DEMO_MARKER} High-yield savings account",
    },
    {
        "account_name": "Chase Sapphire",
        "account_type": "credit_card",
        "institution_name": "Chase Bank",
        "account_number_last4": "9012",
        "opening_balance": Decimal("0.00"),
        "notes": f"{DEMO_MARKER} Chase Sapphire Reserve credit card",
    },
    {
        "account_name": "Amex Gold",
        "account_type": "credit_card",
        "institution_name": "American Express",
        "account_number_last4": "1004",
        "opening_balance": Decimal("0.00"),
        "notes": f"{DEMO_MARKER} Amex Gold rewards card",
    },
    {
        "account_name": "Citi Double Cash",
        "account_type": "credit_card",
        "institution_name": "Citibank",
        "account_number_last4": "7788",
        "opening_balance": Decimal("0.00"),
        "notes": f"{DEMO_MARKER} Citi Double Cash Back card",
    },
    {
        "account_name": "Fidelity HSA",
        "account_type": "other",
        "account_subtype": "hsa",
        "institution_name": "Fidelity Investments",
        "account_number_last4": "3344",
        "has_cash_component": True,
        "opening_balance": Decimal("2500.00"),
        "notes": f"{DEMO_MARKER} Health Savings Account",
    },
    {
        "account_name": "Vanguard Brokerage",
        "account_type": "brokerage",
        "institution_name": "Vanguard",
        "account_number_last4": "5566",
        "has_cash_component": True,
        "has_investment_component": True,
        "opening_balance": Decimal("50000.00"),
        "notes": f"{DEMO_MARKER} Investment brokerage account",
    },
]


# =============================================================================
# Helper Functions
# =============================================================================

def random_amount(min_val: float, max_val: float) -> Decimal:
    """Generate a random amount rounded to cents."""
    return Decimal(str(round(random.uniform(min_val, max_val), 2)))


def random_date_in_month(year: int, month: int) -> date:
    """Generate a random date within the given month."""
    if month == 12:
        next_month = date(year + 1, 1, 1)
    else:
        next_month = date(year, month + 1, 1)

    start = date(year, month, 1)
    days_in_month = (next_month - start).days
    random_day = random.randint(1, days_in_month)
    return date(year, month, random_day)


def get_month_dates(months_back: int = 12) -> list[date]:
    """Get the first day of each month for the past N months."""
    today = date.today()
    dates = []
    for i in range(months_back - 1, -1, -1):
        # Go back i months
        year = today.year
        month = today.month - i
        while month <= 0:
            month += 12
            year -= 1
        dates.append(date(year, month, 1))
    return dates


# =============================================================================
# Category Seeding
# =============================================================================

def seed_demo_categories(db: Session) -> dict[str, int]:
    """
    Seed demo categories if they don't exist.

    Returns:
        dict mapping category_name -> category_id
    """
    print("\n" + "=" * 60)
    print("Seeding Demo Categories")
    print("=" * 60)

    category_map = {}
    added = 0
    skipped = 0

    for cat_data in DEMO_CATEGORIES:
        existing = db.query(Category).filter_by(
            category_name=cat_data["category_name"]
        ).first()

        if existing:
            category_map[cat_data["category_name"]] = existing.category_id
            skipped += 1
        else:
            category = Category(**cat_data)
            db.add(category)
            db.flush()  # Get the ID
            category_map[cat_data["category_name"]] = category.category_id
            added += 1
            print(f"  [ADDED] {cat_data['category_name']}")

    db.commit()
    print(f"\n[OK] Categories: {added} added, {skipped} already existed")
    return category_map


def seed_demo_accounts(db: Session) -> dict[str, int]:
    """
    Seed demo accounts if they don't exist.

    Returns:
        dict mapping account_name -> account_id
    """
    from datetime import date as date_type

    print("\n" + "=" * 60)
    print("Seeding Demo Accounts")
    print("=" * 60)

    account_map = {}
    added = 0
    skipped = 0

    for acct_data in DEMO_ACCOUNTS:
        existing = db.query(Account).filter_by(
            account_name=acct_data["account_name"]
        ).first()

        if existing:
            account_map[acct_data["account_name"]] = existing.account_id
            skipped += 1
        else:
            # Set opening balance date to 13 months ago
            opening_date = date_type.today().replace(day=1)
            if opening_date.month == 1:
                opening_date = opening_date.replace(year=opening_date.year - 2, month=12)
            else:
                opening_date = opening_date.replace(month=opening_date.month - 1)
                if opening_date.year == date_type.today().year:
                    opening_date = opening_date.replace(year=opening_date.year - 1)

            account = Account(
                account_name=acct_data["account_name"],
                account_type=acct_data["account_type"],
                account_subtype=acct_data.get("account_subtype"),
                institution_name=acct_data.get("institution_name"),
                account_number_last4=acct_data.get("account_number_last4"),
                has_cash_component=acct_data.get("has_cash_component", False),
                has_investment_component=acct_data.get("has_investment_component", False),
                opening_balance=acct_data.get("opening_balance", Decimal("0.00")),
                opening_balance_date=opening_date,
                notes=acct_data.get("notes"),
                is_active=True,
            )
            db.add(account)
            db.flush()  # Get the ID
            account_map[acct_data["account_name"]] = account.account_id
            added += 1
            print(f"  [ADDED] {acct_data['account_name']} ({acct_data['account_type']})")

    db.commit()
    print(f"\n[OK] Accounts: {added} added, {skipped} already existed")
    return account_map


def get_classification_map(db: Session) -> dict[str, int]:
    """Get mapping of classification_code -> classification_id."""
    classifications = db.query(TransactionClassification).all()
    return {c.classification_code: c.classification_id for c in classifications}


# =============================================================================
# Income Transaction Generation
# =============================================================================

def generate_income_transactions(
    month_date: date,
    categories: dict[str, int],
    classifications: dict[str, int]
) -> list[dict]:
    """
    Generate income transactions for a given month.

    Args:
        month_date: First day of the month
        categories: Mapping of category_name -> category_id
        classifications: Mapping of classification_code -> classification_id

    Returns:
        List of transaction dicts ready for insertion
    """
    transactions = []
    year, month = month_date.year, month_date.month

    # Salary - 2x per month (1st and 15th)
    employer = random.choice(SALARY_EMPLOYERS)
    salary_amount = random_amount(4500, 6500)

    transactions.append({
        "transaction_date": date(year, month, 1),
        "amount": salary_amount,
        "transaction_type": "Income",
        "category_id": categories["Salary"],
        "classification_id": classifications.get("STANDARD"),
        "description": f"{DEMO_MARKER} Direct Deposit - {employer}",
        "source": employer,
        "payment_method": "Direct Deposit",
    })

    transactions.append({
        "transaction_date": date(year, month, 15),
        "amount": salary_amount,
        "transaction_type": "Income",
        "category_id": categories["Salary"],
        "classification_id": classifications.get("STANDARD"),
        "description": f"{DEMO_MARKER} Direct Deposit - {employer}",
        "source": employer,
        "payment_method": "Direct Deposit",
    })

    # Freelance - 1-3x per month (random)
    num_freelance = random.randint(1, 3)
    for _ in range(num_freelance):
        quarter = (month - 1) // 3 + 1
        client_desc = random.choice(FREELANCE_CLIENTS).format(quarter=quarter)
        transactions.append({
            "transaction_date": random_date_in_month(year, month),
            "amount": random_amount(500, 2000),
            "transaction_type": "Income",
            "category_id": categories["Freelance Income"],
            "classification_id": classifications.get("STANDARD"),
            "description": f"{DEMO_MARKER} {client_desc}",
            "payment_method": "ACH Transfer",
        })

    # Dividends - Quarterly (March, June, September, December)
    if month in [3, 6, 9, 12]:
        for fund in ["VTSAX", "VTIAX", "BND"]:
            transactions.append({
                "transaction_date": random_date_in_month(year, month),
                "amount": random_amount(100, 500),
                "transaction_type": "Income",
                "category_id": categories["Dividends"],
                "classification_id": classifications.get("STANDARD"),
                "description": f"{DEMO_MARKER} Dividend - {fund}",
                "source": "Vanguard",
            })

    # Interest - Monthly (end of month)
    last_day = (date(year, month + 1, 1) if month < 12 else date(year + 1, 1, 1)) - timedelta(days=1)
    transactions.append({
        "transaction_date": last_day,
        "amount": random_amount(5, 50),
        "transaction_type": "Income",
        "category_id": categories["Interest"],
        "classification_id": classifications.get("STANDARD"),
        "description": f"{DEMO_MARKER} Interest - High Yield Savings",
        "source": "Marcus by Goldman Sachs",
    })

    # Refunds - 2-3x per month (random)
    num_refunds = random.randint(2, 3)
    refund_sources = ["Amazon Refund", "Target Return", "Subscription Cancellation", "Price Adjustment"]
    for _ in range(num_refunds):
        transactions.append({
            "transaction_date": random_date_in_month(year, month),
            "amount": random_amount(20, 150),
            "transaction_type": "Income",
            "category_id": categories["Refunds"],
            "classification_id": classifications.get("REFUND"),
            "description": f"{DEMO_MARKER} {random.choice(refund_sources)}",
            "include_in_analysis": True,  # Refunds show as income but classification excludes from calcs
        })

    return transactions


# =============================================================================
# Expense Transaction Generation
# =============================================================================

def generate_expense_transactions(
    month_date: date,
    categories: dict[str, int],
    classifications: dict[str, int]
) -> list[dict]:
    """
    Generate expense transactions for a given month.

    Args:
        month_date: First day of the month
        categories: Mapping of category_name -> category_id
        classifications: Mapping of classification_code -> classification_id

    Returns:
        List of transaction dicts ready for insertion
    """
    transactions = []
    year, month = month_date.year, month_date.month
    standard_class = classifications.get("STANDARD")

    # Rent - 1x per month (1st)
    transactions.append({
        "transaction_date": date(year, month, 1),
        "amount": Decimal("1850.00"),
        "transaction_type": "Expense",
        "category_id": categories["Rent/Mortgage"],
        "classification_id": standard_class,
        "description": f"{DEMO_MARKER} Rent Payment - 123 Main Street Apt 4B",
        "source": PRIMARY_CHECKING,
        "payment_method": "ACH Transfer",
    })

    # Utilities - 3-4x per month
    for util_name, min_amt, max_amt in UTILITY_COMPANIES:
        transactions.append({
            "transaction_date": random_date_in_month(year, month),
            "amount": random_amount(float(min_amt), float(max_amt)),
            "transaction_type": "Expense",
            "category_id": categories["Utilities"],
            "classification_id": standard_class,
            "description": f"{DEMO_MARKER} {util_name}",
            "source": PRIMARY_CHECKING,
            "payment_method": "Auto Pay",
        })

    # Groceries - 4-6x per month
    num_grocery = random.randint(4, 6)
    for _ in range(num_grocery):
        payment = random.choice(["Credit Card", "Debit Card"])
        source = random.choice(CREDIT_CARDS) if payment == "Credit Card" else DEBIT_ACCOUNT
        transactions.append({
            "transaction_date": random_date_in_month(year, month),
            "amount": random_amount(50, 250),
            "transaction_type": "Expense",
            "category_id": categories["Groceries"],
            "classification_id": standard_class,
            "description": f"{DEMO_MARKER} {random.choice(GROCERY_MERCHANTS)}",
            "source": source,
            "payment_method": payment,
        })

    # Dining - 6-10x per month (more in December for holidays)
    num_dining = random.randint(6, 10)
    if month == 12:
        num_dining = random.randint(10, 15)  # Holiday dining
    for _ in range(num_dining):
        transactions.append({
            "transaction_date": random_date_in_month(year, month),
            "amount": random_amount(15, 100),
            "transaction_type": "Expense",
            "category_id": categories["Dining & Restaurants"],
            "classification_id": standard_class,
            "description": f"{DEMO_MARKER} {random.choice(DINING_MERCHANTS)}",
            "source": random.choice(CREDIT_CARDS),
            "payment_method": "Credit Card",
        })

    # Transportation - 4-8x per month
    num_transport = random.randint(4, 8)
    for _ in range(num_transport):
        payment = random.choice(["Credit Card", "Debit Card"])
        source = random.choice(CREDIT_CARDS) if payment == "Credit Card" else DEBIT_ACCOUNT
        transactions.append({
            "transaction_date": random_date_in_month(year, month),
            "amount": random_amount(20, 80),
            "transaction_type": "Expense",
            "category_id": categories["Transportation"],
            "classification_id": standard_class,
            "description": f"{DEMO_MARKER} {random.choice(TRANSPORTATION_MERCHANTS)}",
            "source": source,
            "payment_method": payment,
        })

    # Subscriptions - Fixed amounts on specific days
    for sub_name, sub_amount in SUBSCRIPTION_ITEMS[:random.randint(4, 6)]:
        sub_day = random.randint(1, 28)  # Avoid month-end issues
        transactions.append({
            "transaction_date": date(year, month, sub_day),
            "amount": sub_amount,
            "transaction_type": "Expense",
            "category_id": categories["Subscriptions"],
            "classification_id": standard_class,
            "description": f"{DEMO_MARKER} {sub_name}",
            "source": random.choice(CREDIT_CARDS),
            "payment_method": "Credit Card",
        })

    # Shopping - 3-5x per month (more in November/December)
    num_shopping = random.randint(3, 5)
    if month in [11, 12]:
        num_shopping = random.randint(6, 10)  # Holiday shopping
    for _ in range(num_shopping):
        transactions.append({
            "transaction_date": random_date_in_month(year, month),
            "amount": random_amount(20, 300),
            "transaction_type": "Expense",
            "category_id": categories["Shopping"],
            "classification_id": standard_class,
            "description": f"{DEMO_MARKER} {random.choice(SHOPPING_MERCHANTS)}",
            "source": random.choice(CREDIT_CARDS),
            "payment_method": "Credit Card",
        })

    # Healthcare - 1-2x per month
    num_healthcare = random.randint(1, 2)
    for _ in range(num_healthcare):
        payment = random.choice(["Credit Card", "HSA Card"])
        source = HSA_ACCOUNT if payment == "HSA Card" else random.choice(CREDIT_CARDS)
        transactions.append({
            "transaction_date": random_date_in_month(year, month),
            "amount": random_amount(20, 150),
            "transaction_type": "Expense",
            "category_id": categories["Healthcare"],
            "classification_id": standard_class,
            "description": f"{DEMO_MARKER} {random.choice(HEALTHCARE_MERCHANTS)}",
            "source": source,
            "payment_method": payment,
        })

    # Entertainment - 2-4x per month
    num_entertainment = random.randint(2, 4)
    for _ in range(num_entertainment):
        transactions.append({
            "transaction_date": random_date_in_month(year, month),
            "amount": random_amount(10, 100),
            "transaction_type": "Expense",
            "category_id": categories["Entertainment"],
            "classification_id": standard_class,
            "description": f"{DEMO_MARKER} {random.choice(ENTERTAINMENT_MERCHANTS)}",
            "source": random.choice(CREDIT_CARDS),
            "payment_method": "Credit Card",
        })

    # Insurance - 1x per month
    transactions.append({
        "transaction_date": date(year, month, 15),
        "amount": Decimal("185.00"),
        "transaction_type": "Expense",
        "category_id": categories["Insurance"],
        "classification_id": standard_class,
        "description": f"{DEMO_MARKER} Auto Insurance - GEICO",
        "source": PRIMARY_CHECKING,
        "payment_method": "Auto Pay",
    })

    return transactions


# =============================================================================
# Transfer and Edge Case Generation
# =============================================================================

def generate_transfer_transactions(
    month_date: date,
    categories: dict[str, int],
    classifications: dict[str, int]
) -> list[dict]:
    """
    Generate transfer transactions (internal transfers, CC payments).

    These should be excluded from income/expense calculations.
    """
    transactions = []
    year, month = month_date.year, month_date.month

    transfer_class = classifications.get("TRANSFER")
    cc_payment_class = classifications.get("CC_PAYMENT")
    cc_receipt_class = classifications.get("CC_RECEIPT")

    # Internal transfers - 2-3 per month
    num_transfers = random.randint(2, 3)
    for _ in range(num_transfers):
        transfer_amount = random_amount(500, 2000)
        transfer_date = random_date_in_month(year, month)

        # Expense side (from checking)
        transactions.append({
            "transaction_date": transfer_date,
            "amount": transfer_amount,
            "transaction_type": "Expense",
            "category_id": categories["Transfers"],
            "classification_id": transfer_class,
            "description": f"{DEMO_MARKER} Transfer to Savings Account",
            "source": PRIMARY_CHECKING,
            "is_transfer": True,
            "include_in_analysis": False,
            "transfer_account_from": PRIMARY_CHECKING,
            "transfer_account_to": SAVINGS_ACCOUNT,
        })

        # Income side (to savings)
        transactions.append({
            "transaction_date": transfer_date,
            "amount": transfer_amount,
            "transaction_type": "Income",
            "category_id": categories["Transfers"],
            "classification_id": transfer_class,
            "description": f"{DEMO_MARKER} Transfer from Checking Account",
            "source": SAVINGS_ACCOUNT,
            "is_transfer": True,
            "include_in_analysis": False,
            "transfer_account_from": PRIMARY_CHECKING,
            "transfer_account_to": SAVINGS_ACCOUNT,
        })

    # Credit card payment - 1 pair per month
    cc_amount = random_amount(1500, 3500)
    cc_date = random_date_in_month(year, month)
    cc_card = random.choice(CREDIT_CARDS)

    # Payment from checking (expense)
    transactions.append({
        "transaction_date": cc_date,
        "amount": cc_amount,
        "transaction_type": "Expense",
        "category_id": categories["Credit Card Payment"],
        "classification_id": cc_payment_class,
        "description": f"{DEMO_MARKER} Payment to {cc_card}",
        "source": PRIMARY_CHECKING,
        "is_transfer": True,
        "include_in_analysis": False,
        "payment_method": "ACH Transfer",
    })

    # Receipt on credit card (income to CC account)
    transactions.append({
        "transaction_date": cc_date,
        "amount": cc_amount,
        "transaction_type": "Income",
        "category_id": categories["Credit Card Payment"],
        "classification_id": cc_receipt_class,
        "description": f"{DEMO_MARKER} Payment Received - {cc_card}",
        "source": cc_card,
        "is_transfer": True,
        "include_in_analysis": False,
    })

    return transactions


def generate_edge_cases(
    month_date: date,
    categories: dict[str, int],
    classifications: dict[str, int],
    month_index: int
) -> list[dict]:
    """
    Generate data quality edge cases for testing warnings.

    Only generates these for certain months to spread them out.
    """
    transactions = []
    year, month = month_date.year, month_date.month

    reimb_paid_class = classifications.get("REIMB_PAID")
    reimb_recv_class = classifications.get("REIMB_RECEIVED")
    capital_class = classifications.get("CAPITAL_EXPENSE")
    standard_class = classifications.get("STANDARD")

    # Reimbursement pair - every other month
    if month_index % 2 == 0:
        reimb_amount = random_amount(100, 400)
        reimb_date = random_date_in_month(year, month)

        # Expense paid (will be reimbursed)
        transactions.append({
            "transaction_date": reimb_date,
            "amount": reimb_amount,
            "transaction_type": "Expense",
            "category_id": categories["Shopping"],  # Work supplies
            "classification_id": reimb_paid_class,
            "description": f"{DEMO_MARKER} Work Supplies - To Be Reimbursed",
            "notes": "Submit expense report",
        })

        # Reimbursement received (a few days later)
        transactions.append({
            "transaction_date": reimb_date + timedelta(days=random.randint(5, 14)),
            "amount": reimb_amount,
            "transaction_type": "Income",
            "category_id": categories["Reimbursements"],
            "classification_id": reimb_recv_class,
            "description": f"{DEMO_MARKER} Expense Reimbursement - Work Supplies",
            "include_in_analysis": False,  # Excluded from income calcs
        })

    # Capital expense - once every 4 months
    if month_index % 4 == 0:
        capital_items = [
            ("New Laptop - MacBook Pro", Decimal("2499.00")),
            ("Office Furniture", Decimal("850.00")),
            ("Home Appliance - Refrigerator", Decimal("1200.00")),
        ]
        item_name, item_amount = random.choice(capital_items)
        transactions.append({
            "transaction_date": random_date_in_month(year, month),
            "amount": item_amount,
            "transaction_type": "Expense",
            "category_id": categories["Shopping"],
            "classification_id": capital_class,
            "description": f"{DEMO_MARKER} {item_name}",
            "notes": "Capital expense - excluded from operating expenses",
        })

    # Data quality issues - only in specific months
    # Miscategorized item (expense category marked as income) - month 3, 7
    if month_index in [2, 6]:
        transactions.append({
            "transaction_date": random_date_in_month(year, month),
            "amount": random_amount(50, 150),
            "transaction_type": "Income",  # WRONG - should be expense
            "category_id": categories["Groceries"],  # Expense category as income = warning
            "classification_id": standard_class,
            "description": f"{DEMO_MARKER} Safeway - MISCATEGORIZED",
            "notes": "Data quality test - expense marked as income",
        })

    # Uncategorized transactions - spread across months
    if month_index % 3 == 0:
        for _ in range(random.randint(1, 3)):
            transactions.append({
                "transaction_date": random_date_in_month(year, month),
                "amount": random_amount(25, 200),
                "transaction_type": random.choice(["Income", "Expense"]),
                "category_id": categories["Uncategorized"],
                "classification_id": standard_class,
                "description": f"{DEMO_MARKER} Unknown Transaction - Needs Review",
                "notes": "Data quality test - uncategorized",
            })

    # Outlier amount - month 5, 10
    if month_index in [4, 9]:
        transactions.append({
            "transaction_date": random_date_in_month(year, month),
            "amount": random_amount(5000, 10000),  # Unusually high
            "transaction_type": "Expense",
            "category_id": categories["Shopping"],
            "classification_id": standard_class,
            "description": f"{DEMO_MARKER} Large Purchase - OUTLIER",
            "notes": "Data quality test - outlier amount",
        })

    return transactions


# =============================================================================
# Main Seeding Functions
# =============================================================================

def seed_demo_transactions(db: Session, months: int = DEMO_MONTHS) -> dict:
    """
    Seed demo transactions for the specified number of months.

    Args:
        db: Database session
        months: Number of months of data to generate (default: 12)

    Returns:
        dict with counts of created transactions
    """
    print("\n" + "=" * 60)
    print("Seeding Demo Transaction Data")
    print("=" * 60)

    # Set random seed for reproducibility
    random.seed(RANDOM_SEED)

    # Seed accounts first
    accounts = seed_demo_accounts(db)

    # Seed categories
    categories = seed_demo_categories(db)

    # Get classification mappings
    classifications = get_classification_map(db)
    if not classifications:
        print("[ERROR] No classifications found. Run init_db first.")
        return {"total": 0, "error": "No classifications"}

    # Generate transactions for each month
    month_dates = get_month_dates(months)

    total_income = 0
    total_expense = 0
    total_transfers = 0
    total_edge_cases = 0

    print(f"\nGenerating transactions for {months} months...")

    for i, month_date in enumerate(month_dates):
        month_name = month_date.strftime("%B %Y")

        # Generate all transaction types
        income_txns = generate_income_transactions(month_date, categories, classifications)
        expense_txns = generate_expense_transactions(month_date, categories, classifications)
        transfer_txns = generate_transfer_transactions(month_date, categories, classifications)
        edge_txns = generate_edge_cases(month_date, categories, classifications, i)

        # Combine and insert
        all_txns = income_txns + expense_txns + transfer_txns + edge_txns

        for txn_data in all_txns:
            transaction = Transaction(**txn_data)
            db.add(transaction)

        total_income += len(income_txns)
        total_expense += len(expense_txns)
        total_transfers += len(transfer_txns)
        total_edge_cases += len(edge_txns)

        print(f"  {month_name}: {len(all_txns)} transactions")

    db.commit()

    total = total_income + total_expense + total_transfers + total_edge_cases

    print("\n" + "-" * 40)
    print(f"[OK] Demo data seeding complete!")
    print(f"     Income transactions:   {total_income}")
    print(f"     Expense transactions:  {total_expense}")
    print(f"     Transfer pairs:        {total_transfers}")
    print(f"     Edge cases:            {total_edge_cases}")
    print(f"     TOTAL:                 {total}")
    print("-" * 40)

    return {
        "total": total,
        "income": total_income,
        "expense": total_expense,
        "transfers": total_transfers,
        "edge_cases": total_edge_cases,
    }


def clear_demo_data(db: Session) -> dict:
    """
    Remove all demo data (transactions and accounts identified by DEMO_MARKER).

    Args:
        db: Database session

    Returns:
        dict with counts of deleted transactions and accounts
    """
    print("\n" + "=" * 60)
    print("Clearing Demo Data")
    print("=" * 60)

    # Find all demo transactions
    demo_txns = db.query(Transaction).filter(
        Transaction.description.like(f"%{DEMO_MARKER}%")
    ).all()

    txn_count = len(demo_txns)

    if txn_count > 0:
        # First, clear related_transaction_id to avoid circular dependency
        demo_ids = [txn.transaction_id for txn in demo_txns]
        db.query(Transaction).filter(
            Transaction.transaction_id.in_(demo_ids)
        ).update({Transaction.related_transaction_id: None}, synchronize_session=False)
        db.flush()

        # Delete them using bulk delete to avoid ORM dependency issues
        db.query(Transaction).filter(
            Transaction.transaction_id.in_(demo_ids)
        ).delete(synchronize_session=False)

        print(f"[OK] Deleted {txn_count} demo transactions.")
    else:
        print("[OK] No demo transactions found.")

    # Find and delete demo accounts (identified by DEMO_MARKER in notes)
    demo_accounts = db.query(Account).filter(
        Account.notes.like(f"%{DEMO_MARKER}%")
    ).all()

    acct_count = len(demo_accounts)

    if acct_count > 0:
        demo_acct_ids = [acct.account_id for acct in demo_accounts]
        db.query(Account).filter(
            Account.account_id.in_(demo_acct_ids)
        ).delete(synchronize_session=False)

        print(f"[OK] Deleted {acct_count} demo accounts.")
    else:
        print("[OK] No demo accounts found.")

    db.commit()

    return {"transactions": txn_count, "accounts": acct_count}


# =============================================================================
# CLI Entry Point
# =============================================================================

def main():
    """CLI entry point for demo data seeding."""
    parser = argparse.ArgumentParser(
        description="Seed demo transaction data for the financial analysis app"
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Clear existing demo data before seeding"
    )
    parser.add_argument(
        "--clear-only",
        action="store_true",
        help="Only clear demo data, don't seed new data"
    )
    parser.add_argument(
        "--months",
        type=int,
        default=DEMO_MONTHS,
        help=f"Number of months of data to generate (default: {DEMO_MONTHS})"
    )

    args = parser.parse_args()

    db = SessionLocal()
    try:
        if args.reset or args.clear_only:
            clear_result = clear_demo_data(db)
            if args.clear_only:
                print(f"\n[SUCCESS] Cleared {clear_result['transactions']} transactions, {clear_result['accounts']} accounts")

        if not args.clear_only:
            result = seed_demo_transactions(db, months=args.months)
            print(f"\n[SUCCESS] Created {result['total']} demo transactions")

    except Exception as e:
        print(f"\n[ERROR] {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
