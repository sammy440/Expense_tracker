from collections import defaultdict
from datetime import datetime

def get_total_spending(expenses):
    """Calculate total spending from a list of expenses."""
    return sum(float(item['amount']) for item in expenses)

def get_expense_count(expenses):
    """Return the total number of expenses."""
    return len(expenses)

def get_category_breakdown(expenses):
    """Return a dictionary of total spending per category."""
    breakdown = defaultdict(float)
    for item in expenses:
        breakdown[item['category']] += float(item['amount'])
    return dict(breakdown)

def get_highest_spending_category(expenses):
    """Return the category with the highest spending."""
    breakdown = get_category_breakdown(expenses)
    if not breakdown:
        return "N/A"
    return max(breakdown, key=breakdown.get)

def get_monthly_spending(expenses):
    """Return a dictionary of spending per month (YYYY-MM)."""
    monthly = defaultdict(float)
    for item in expenses:
        # Assuming date format is YYYY-MM-DD or similar that can be parsed
        # If date is stored as string, we might need to parse it.
        # Let's assume standard ISO format or similar for now.
        try:
            date_obj = datetime.strptime(item['date'], "%Y-%m-%d")
            month_key = date_obj.strftime("%Y-%m")
            monthly[month_key] += float(item['amount'])
        except ValueError:
            continue # Skip invalid dates
    return dict(monthly)
