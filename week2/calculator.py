'''Business Profit Calculator: Calculates profit and margin percentage from revenue and cost data'''
import re

def get_float(prompt):
    pattern = r"^\d{1,3}(,\d{3})*(\.\d+)?$|^\d+(\.\d+)?$"
    
    while True:
        user_input = input(prompt)
        
        if not re.match(pattern, user_input):
            print("Invalid format. Use e.g. 1,000.50 or 1000.50")
            continue
        
        cleaned = user_input.replace(",", "") # remove commas: this approach assumes: comma = thousands separator (US/UK style), not applicable for countries where comma = decimal (e.g DE)
        return float(cleaned)

revenue = get_float("Enter total revenue: $")
costs = get_float("Enter total costs: $")
# Calculate profit
profit = revenue - costs
# Calculate profit margin percentage
margin = (profit / revenue) * 100
# Display results
print("\n--- Financial Summary ---")
print(f"Revenue: ${revenue:,.2f}")
print(f"Costs: ${costs:,.2f}")
print(f"Profit: ${profit:,.2f}")
print(f"Profit Margin: {margin:.1f}%")