# Exercise 3: Personal Expense Tracker

# Initialize Data Structures
expense_records = []      # list of tuples (category, amount, date)
category_totals = {}      # dict: category -> total amount spent
unique_categories = set() # set of all categories used
overall_stats = {}        # dict for total, average, highest, lowest expenses

# Collect Expense Data
num_expenses = 5  # I chose 5 here
print("PERSONAL EXPENSE TRACKER\n")
for i in range(1, num_expenses + 1):
    print(f"Enter expense {i}:")
    category = input("Category: ")
    amount = float(input("Amount: $"))
    date = input("Date (YYYY-MM-DD): ")
    
    expense_records.append((category, amount, date))
    
    category_totals[category] = category_totals.get(category, 0.0) + amount
    
    unique_categories.add(category)
    print()  

# Calculate Overall Statistics
amounts = [amt for (_, amt, _) in expense_records]

total_spending = sum(amounts)
average_expense = total_spending / len(amounts)
highest_expense = max(amounts)
lowest_expense = min(amounts)

# Find category & date of highest and lowest expense
highest_info = None
lowest_info = None
for cat, amt, dt in expense_records:
    if amt == highest_expense:
        highest_info = (cat, dt)
    if amt == lowest_expense:
        lowest_info = (cat, dt)

overall_stats = {
    "total": total_spending,
    "average": average_expense,
    "highest": (highest_expense, highest_info),
    "lowest": (lowest_expense, lowest_info)
}

# Generate Spending Report
print("\n==== OVERALL SPENDING SUMMARY ====")
print(f"Total Spending: ${total_spending:.2f}")
print(f"Average Expense: ${average_expense:.2f}")
print(f"Highest Expense: ${highest_expense:.2f} (Category: {highest_info[0]}, Date: {highest_info[1]})")
print(f"Lowest Expense: ${lowest_expense:.2f} (Category: {lowest_info[0]}, Date: {lowest_info[1]})")

print("\n==== UNIQUE CATEGORIES SPENT ON ====")
print(tuple(unique_categories))
print(f"Total unique categories: {len(unique_categories)}")

print("\n==== SPENDING BY CATEGORY ====")
for category, total in category_totals.items():
    print(f"{category}: ${total:.2f}")


# Challenge Extensions
import json
import csv
from collections import defaultdict
from datetime import datetime

# 1. Input validation helpers
def validate_amount(amount_str):
    """Return float if valid, else raise ValueError"""
    try:
        amt = float(amount_str)
        if amt < 0:
            raise ValueError("Amount cannot be negative")
        return amt
    except ValueError:
        raise ValueError("Invalid amount. Please enter a positive number")

def validate_date(date_str):
    """Return datetime.date if format is valid: YYYY-MM-DD, else raise ValueError"""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Invalid date. Use YYYY-MM-DD format")

# 2. Filter expenses by category or date range
def filter_expenses(records, category=None, start_date=None, end_date=None):
    """
    records: list of (category, amount, date) with date as string YYYY-MM-DD
    Returns filtered list
    """
    filtered = []
    for cat, amt, dt_str in records:
        dt = datetime.strptime(dt_str, "%Y-%m-%d").date()
        if category and cat.lower() != category.lower():
            continue
        if start_date and dt < start_date:
            continue
        if end_date and dt > end_date:
            continue
        filtered.append((cat, amt, dt_str))
    return filtered

# 3. Save and load data to/from JSON or CSV
def save_to_json(records, filename="expenses.json"):
    """Save expense_records to JSON file"""
    data = [{"category": c, "amount": a, "date": d} for c, a, d in records]
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Saved {len(records)} expenses to {filename}")

def load_from_json(filename="expenses.json"):
    """Load expense_records from JSON file"""
    with open(filename, "r") as f:
        data = json.load(f)
    return [(item["category"], item["amount"], item["date"]) for item in data]

def save_to_csv(records, filename="expenses.csv"):
    """Save expenses to CSV file"""
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Category", "Amount", "Date"])
        writer.writerows(records)
    print(f"Saved to {filename}")

def load_from_csv(filename="expenses.csv"):
    """Load expenses from CSV file"""
    records = []
    with open(filename, "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if len(row) == 3:
                records.append((row[0], float(row[1]), row[2]))
    return records

# 4. ASCII bar chart for spending by category
def ascii_bar_chart(category_totals, max_width=30):
    """Print a horizontal bar chart"""
    if not category_totals:
        print("No data to chart")
        return
    max_amount = max(category_totals.values())
    print("\n SPENDING BAR CHART (ASCII) ")
    for cat, total in sorted(category_totals.items(), key=lambda x: x[1], reverse=True):
        bar_length = int((total / max_amount) * max_width) if max_amount > 0 else 0
        bar = "#" * bar_length
        print(f"{cat:12} | {bar} ${total:.2f}")

# 5. Monthly/weekly spending averages if multiple dates are provided
def spending_by_period(records, period="month"):
    """
    period: 'month' or 'week'
    Returns dict of period -> total spent
    """
    period_totals = defaultdict(float)
    for cat, amt, dt_str in records:
        dt = datetime.strptime(dt_str, "%Y-%m-%d").date()
        if period == "month":
            key = dt.strftime("%Y-%m")
        elif period == "week":
            key = f"{dt.year}-W{dt.isocalendar()[1]:02d}"
        else:
            raise ValueError("period must be 'month' or 'week'")
        period_totals[key] += amt
    return dict(period_totals)

# Demo
if __name__ == "__main__":
    # 1. Filter example
    food_expenses = filter_expenses(expense_records, category="Food") #Filtered Example Food here
    print(f"\nFood expenses: {len(food_expenses)} items")
    
    # 2. Save to JSON
    save_to_json(expense_records)
    
    # 3. ASCII chart
    ascii_bar_chart(category_totals)
    
    # 4. Monthly totals
    monthly = spending_by_period(expense_records, "month")
    print("\nMonthly spending:", monthly)