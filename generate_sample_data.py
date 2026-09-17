# makes fake sales data lol
# run it and it creates a fake csv with 1000 orders
# its fake data but looks kinda real

import random
from datetime import datetime, timedelta
import csv
import os

# fake names and stuff
CATEGORIES = {
    "Electronics": ["Smartphone", "Laptop", "Headphones", "Smartwatch", "Tablet"],
    "Furniture": ["Office Chair", "Desk", "Bookshelf", "Sofa", "Lamp"],
    "Office Supplies": ["Pen Pack", "Notebook", "Stapler", "Paper Ream", "Folder"],
    "Clothing": ["T-Shirt", "Jeans", "Sneakers", "Jacket", "Hat"],
    "Toys": ["Puzzle", "Board Game", "Action Figure", "Doll", "RC Car"],
}

REGIONS = ["North", "South", "East", "West", "Central"]
CUSTOMERS = [f"CUST-{1000+i}" for i in range(120)]
CHANNELS = ["Online", "Store", "Partner"]

# same data every time you run it
random.seed(42)


def random_date_in_2024():
    # random date in 2024
    start = datetime(2024, 1, 1)
    end = datetime(2024, 12, 31)
    delta = (end - start).days
    return (start + timedelta(days=random.randint(0, delta))).strftime("%Y-%m-%d")


def random_row(order_id):
    # makes one fake row
    category = random.choice(list(CATEGORIES.keys()))
    product = random.choice(CATEGORIES[category])
    quantity = random.randint(1, 5)
    unit_price = round(random.uniform(10, 800), 2)
    discount = random.choice([0.0, 0.0, 0.05, 0.10, 0.15, 0.20, 0.25])
    # sometimes negative profit = the "anomalies" in the analysis
    profit = round((unit_price * quantity) * random.uniform(-0.15, 0.35), 2)
    return {
        "OrderID": f"ORD-{10000+order_id}",
        "OrderDate": random_date_in_2024(),
        "CustomerID": random.choice(CUSTOMERS),
        "Region": random.choice(REGIONS),
        "Channel": random.choice(CHANNELS),
        "Category": category,
        "Product": product,
        "Quantity": quantity,
        "UnitPrice": unit_price,
        "Discount": discount,
        "Sales": round(unit_price * quantity * (1 - discount), 2),
        "Profit": profit,
    }


def main():
    # make the data folder if it doesnt exist
    here = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(here, "data")
    os.makedirs(data_dir, exist_ok=True)

    output_path = os.path.join(data_dir, "sales_sample.csv")
    number_of_rows = 1000

    # write the csv
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "OrderID", "OrderDate", "CustomerID", "Region", "Channel",
            "Category", "Product", "Quantity", "UnitPrice", "Discount",
            "Sales", "Profit"
        ])
        writer.writeheader()
        for i in range(number_of_rows):
            writer.writerow(random_row(i))

    print(f"[OK] Generated {number_of_rows} rows at: {output_path}")


if __name__ == "__main__":
    main()