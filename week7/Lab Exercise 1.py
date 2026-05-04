# Lab Exercise 1: Product Pricing Manager
category_discount = {
    "Electronics": 10,   # percentage
    "Clothing": 15,
    "Books": 5,
    "Home": 12
}

tier_discount = {
    "Premium": 5,
    "Standard": 0,
    "Budget": 2
}

#Open and read the input file
try:
    with open("products.txt", "r") as file:
        lines = file.readlines()
except FileNotFoundError:
    print("Error: products.txt not found")
    exit()
except PermissionError:
    print("Error: Cannot read the file products.txt")
    exit()

#Write output
output_lines = []
output_lines.append("PRODUCT PRICING REPORT\n")
output_lines.append(f"{'Product':<25} {'Base':>8} {'Disc%':>6} {'Disc $':>9} {'Final':>9}\n")
output_lines.append("-" * 60 + "\n")

total_products = 0
total_discount_percent = 0

for line in lines:
    line = line.strip()
    if not line:
        continue
    
#Split by comma
    parts = line.split(",")
    if len(parts) != 4:
        print(f"Skipping invalid line: {line}")
        continue
    
    name = parts[0].strip()
    price_str = parts[1].strip()
    category = parts[2].strip()
    tier = parts[3].strip()
    
#Convert price to number
    try:
        base_price = float(price_str)
        if base_price < 0:
            raise ValueError
    except ValueError:
        print(f"Invalid price '{price_str}' for {name}. Skipping.")
        continue
    
#Get discounts (default to 0 if category/tier not found)
    cat_disc = category_discount.get(category, 0)
    tier_disc = tier_discount.get(tier, 0)
    total_disc_percent = cat_disc + tier_disc
    discount_amount = base_price * (total_disc_percent / 100)
    final_price = base_price - discount_amount
    
#Add to report
    output_lines.append(f"{name:<25} ${base_price:>6.2f} {total_disc_percent:>5}% ${discount_amount:>7.2f} ${final_price:>7.2f}\n")
    
    total_products += 1
    total_discount_percent += total_disc_percent

#Write output file
try:
    with open("pricing_report.txt", "w") as out:
        out.writelines(output_lines)
    print(f"Report written as pricing_report.txt")
except PermissionError:
    print("Error: Cannot write as pricing_report.txt")
    exit()

#Summary
if total_products > 0:
    avg_discount = total_discount_percent / total_products
    print(f"Total products processed: {total_products}")
    print(f"Average discount: {avg_discount:.2f}%")
else:
    print("No valid products were processed")