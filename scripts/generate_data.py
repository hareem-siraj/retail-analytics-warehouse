import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)  # For reproducibility

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / 'data' / 'sample'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def write_csv(file_name,rows):
    if not rows:
        raise ValueError(f'No data provided for {file_name}')

    path  = OUTPUT_DIR / file_name

    with path.open('w', newline = '', encoding = 'utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f'created {path.name}: {len(rows)} rows')


# --------------------------------------------------
# 1. CUSTOMERS
# --------------------------------------------------

first_names = [
    "Alex", "Sam", "Jordan", "Taylor", "Morgan",
    "Jamie", "Chris", "Robin", "Casey", "Avery"
]

last_names = [
    "Miller", "Schmidt", "Weber", "Fischer", "Brown",
    "Wilson", "Khan", "Ali", "Smith", "Meyer"
]

cities = [
    "Berlin", "Hamburg", "Munich", "Frankfurt",
    "Cologne", "Marburg", "Stuttgart", "Leipzig"
]

customers = []

for i in range(1, 101):
    first = random.choice(first_names)
    last = random.choice(last_names)
    city = random.choice(cities)

    # Deliberately introduce inconsistent capitalization.
    if i % 13 == 0:
        city = city.upper()

    # Deliberately introduce missing emails.
    email = (
        ""
        if i % 19 == 0
        else f"customer{i}@example.com"
    )

    customers.append({
        "customer_id": f"C{i:04d}",
        "customer_name": f"{first} {last}",
        "email": email,
        "city": city,
        "segment": random.choice(["Consumer", "Business", "Small Business"]),
        "updated_at": (
            datetime(2026, 10, 1) + timedelta(days=i)
        ).isoformat(timespec="seconds"),
    })


# --------------------------------------------------
# 2. PRODUCTS
# --------------------------------------------------

categories = ["Electronics", "Home", "Clothing", "Sports", "Books"]

products = []

for i in range(1, 31):
    products.append({
        "product_id": f"P{i:03d}",
        "product_name": f"Product {i:03d}",
        "category": categories[(i - 1) % len(categories)],
        "unit_price": round(random.uniform(8, 500), 2),
    })


# --------------------------------------------------
# 3. ORDERS
# --------------------------------------------------

orders = []
base_date = datetime(2025, 1, 1)

for i in range(1, 1201):
    order_date = base_date + timedelta(
        days=random.randint(0, 638)
    )

    # Most dates use ISO format; some use DD/MM/YYYY.
    if i % 17 == 0:
        formatted_date = order_date.strftime("%d/%m/%Y")
    else:
        formatted_date = order_date.strftime("%Y-%m-%d")

    customer_id = f"C{random.randint(1, 100):04d}"
    product_id = f"P{random.randint(1, 30):03d}"

    quantity = random.randint(1, 5)
    unit_price = next(
        p["unit_price"]
        for p in products
        if p["product_id"] == product_id
    )

    # Deliberately introduce invalid quantities.
    if i % 89 == 0:
        quantity = 0

    # Deliberately introduce invalid prices.
    if i % 97 == 0:
        unit_price = -abs(unit_price)

    # Deliberately introduce unknown customer/product references.
    if i % 113 == 0:
        customer_id = "C9999"

    if i % 131 == 0:
        product_id = "P999"

    # Deliberately vary status capitalization.
    status = random.choice(["completed", "pending", "cancelled"])
    if i % 23 == 0:
        status = status.upper()

    loaded_at = datetime(2026, 10, 1) + timedelta(minutes=i)

    row = {
        "order_line_id": f"OL{i:06d}",
        "order_id": f"O{((i - 1) // 3) + 1:05d}",
        "customer_id": customer_id,
        "product_id": product_id,
        "order_date": formatted_date,
        "quantity": quantity,
        "unit_price": unit_price,
        "status": status,
        "updated_at": loaded_at.isoformat(timespec="seconds"),
        "loaded_at": loaded_at.isoformat(timespec="seconds"),
    }

    orders.append(row)

    # Deliberately duplicate some source records.
    if i % 100 == 0:
        duplicate = row.copy()
        duplicate["loaded_at"] = (
            loaded_at + timedelta(minutes=1)
        ).isoformat(timespec="seconds")
        orders.append(duplicate)


# Save all datasets.
write_csv("customers.csv", customers)
write_csv("products.csv", products)
write_csv("orders.csv", orders)

print("\nRetail sample data generation complete.")
