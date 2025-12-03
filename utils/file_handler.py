import json
import os
import csv

DATA_FILE = "expenses.json"

def load_expenses():
    """Load expenses from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_expenses(expenses):
    """Save the list of expenses to the JSON file."""
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(expenses, f, indent=4)
        return True
    except IOError:
        return False

def add_expense(expense):
    """Add a new expense dictionary to the list and save."""
    expenses = load_expenses()
    expenses.append(expense)
    return save_expenses(expenses)

def export_to_csv(filename="expenses.csv"):
    """Export all expenses to a CSV file."""
    expenses = load_expenses()
    if not expenses:
        return False
    
    keys = expenses[0].keys()
    try:
        with open(filename, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(expenses)
        return True
    except IOError:
        return False
