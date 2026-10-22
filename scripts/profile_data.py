import csv
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT/ 'data' / 'sample'


def read_csv(filename):
    path = DATA_DIR/filename

    with path.open('r', newline='', encoding = 'utf-8') as file:
        return list(csv.DictReader(file))


customers = read_csv('customers.csv')
products = read_csv('products.csv')
orders = read_csv('orders.csv')


print('=' * 50)
print('RETAIL DATA QUALITY PROFILE')
print('=' * 50)

# 1. Dataset sizes
print("\n1. ROW COUNTS")
print(f"Customers: {len(customers)}")
print(f"Products:  {len(products)}")
print(f"Orders:    {len(orders)}")

# 2. Missing customer emails
missing_emails = [
    row for row in customers
    if not row["email"].strip()
]
print(f"\n2. CUSTOMERS WITH MISSING EMAILS: {len(missing_emails)}")

# 3. Duplicate order-line IDs
order_line_ids = [row["order_line_id"] for row in orders]
duplicate_ids = len(order_line_ids) - len(set(order_line_ids))
print(f"\n3. DUPLICATE ORDER-LINE IDs: {duplicate_ids}")

# 4. Invalid quantities and prices
invalid_quantities = [
    row for row in orders
    if int(row["quantity"]) <= 0
]

invalid_prices = [
    row for row in orders
    if float(row["unit_price"]) <= 0
]

print(f"\n4. INVALID QUANTITIES (<= 0): {len(invalid_quantities)}")
print(f"5. INVALID UNIT PRICES (<= 0): {len(invalid_prices)}")

# 6. Unknown customer references
customer_ids = {row["customer_id"] for row in customers}

unknown_customers = [
    row for row in orders
    if row["customer_id"] not in customer_ids
]
print(f"\n6. ORDERS WITH UNKNOWN CUSTOMERS: {len(unknown_customers)}")

# 7. Unknown product references
product_ids = {row["product_id"] for row in products}

unknown_products = [
    row for row in orders
    if row["product_id"] not in product_ids
]
print(f"7. ORDERS WITH UNKNOWN PRODUCTS: {len(unknown_products)}")

# 8. Inconsistent status capitalization
statuses = {row["status"] for row in orders}
print(f"\n8. DISTINCT RAW ORDER STATUSES: {sorted(statuses)}")

# 9. Show a few problematic records
print("\n9. EXAMPLE INVALID QUANTITIES")
for row in invalid_quantities[:3]:
    print(
        f"Order line: {row['order_line_id']}, "
        f"quantity: {row['quantity']}"
    )

print("\nProfiling complete.")