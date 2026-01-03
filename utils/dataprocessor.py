from collections import defaultdict
from datetime import datetime

def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions
    """
    total_revenue = 0.0

    for t in transactions:
        total_revenue += t['Quantity'] * t['UnitPrice']

    return round(total_revenue, 2)

# Region-wise Sales Analysis

def region_wise_sales(transactions):
    """
    Analyzes sales by region
    """
    region_data = defaultdict(lambda: {
        'total_sales': 0.0,
        'transaction_count': 0
    })

    total_sales_all = 0.0

    for t in transactions:
        amount = t['Quantity'] * t['UnitPrice']
        region = t['Region']

        region_data[region]['total_sales'] += amount
        region_data[region]['transaction_count'] += 1
        total_sales_all += amount

    result = {}

    for region, data in region_data.items():
        percentage = (
            (data['total_sales'] / total_sales_all) * 100
            if total_sales_all > 0 else 0
        )

        result[region] = {
            'total_sales': round(data['total_sales'], 2),
            'transaction_count': data['transaction_count'],
            'percentage': round(percentage, 2)
        }

    # Sort by total_sales descending
    result = dict(
        sorted(
            result.items(),
            key=lambda x: x[1]['total_sales'],
            reverse=True
        )
    )

    return result


# (c) Top Selling Products

def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold
    """
    product_data = defaultdict(lambda: {
        'quantity': 0,
        'revenue': 0.0
    })

    for t in transactions:
        name = t['ProductName']
        qty = t['Quantity']
        revenue = qty * t['UnitPrice']

        product_data[name]['quantity'] += qty
        product_data[name]['revenue'] += revenue

    aggregated = [
        (name,
         data['quantity'],
         round(data['revenue'], 2))
        for name, data in product_data.items()
    ]

    aggregated.sort(key=lambda x: x[1], reverse=True)

    return aggregated[:n]


# (d) Customer Purchase Analysis

def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns
    """
    customer_data = defaultdict(lambda: {
        'total_spent': 0.0,
        'purchase_count': 0,
        'products': set()
    })

    for t in transactions:
        customer = t['CustomerID']
        amount = t['Quantity'] * t['UnitPrice']

        customer_data[customer]['total_spent'] += amount
        customer_data[customer]['purchase_count'] += 1
        customer_data[customer]['products'].add(t['ProductName'])

    result = {}

    for customer, data in customer_data.items():
        avg_value = (
            data['total_spent'] / data['purchase_count']
            if data['purchase_count'] > 0 else 0
        )

        result[customer] = {
            'total_spent': round(data['total_spent'], 2),
            'purchase_count': data['purchase_count'],
            'avg_order_value': round(avg_value, 2),
            'products_bought': sorted(list(data['products']))
        }

    # Sort by total_spent descending
    result = dict(
        sorted(
            result.items(),
            key=lambda x: x[1]['total_spent'],
            reverse=True
        )
    )

    return result

# Daily Sales Trend

def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date
    """
    daily_data = defaultdict(lambda: {
        'revenue': 0.0,
        'transaction_count': 0,
        'customers': set()
    })

    for t in transactions:
        date = t['Date']
        amount = t['Quantity'] * t['UnitPrice']

        daily_data[date]['revenue'] += amount
        daily_data[date]['transaction_count'] += 1
        daily_data[date]['customers'].add(t['CustomerID'])

    result = {}

    for date in sorted(daily_data.keys(), key=lambda d: datetime.strptime(d, '%Y-%m-%d')):
        data = daily_data[date]

        result[date] = {
            'revenue': round(data['revenue'], 2),
            'transaction_count': data['transaction_count'],
            'unique_customers': len(data['customers'])
        }

    return result

# Peak Sales Day

def find_peak_sales_day(transactions):
    """
    Identifies the date with highest revenue
    """
    daily_totals = defaultdict(lambda: {
        'revenue': 0.0,
        'transaction_count': 0
    })

    for t in transactions:
        date = t['Date']
        amount = t['Quantity'] * t['UnitPrice']

        daily_totals[date]['revenue'] += amount
        daily_totals[date]['transaction_count'] += 1

    peak_date = None
    max_revenue = 0.0

    for date, data in daily_totals.items():
        if data['revenue'] > max_revenue:
            max_revenue = data['revenue']
            peak_date = date

    return (
        peak_date,
        round(max_revenue, 2),
        daily_totals[peak_date]['transaction_count']
    )

# Low Performing Products

def low_performing_products(transactions, threshold=10):
    """
    Identifies products with low sales
    """
    product_data = defaultdict(lambda: {
        'quantity': 0,
        'revenue': 0.0
    })

    for t in transactions:
        name = t['ProductName']
        qty = t['Quantity']
        revenue = qty * t['UnitPrice']

        product_data[name]['quantity'] += qty
        product_data[name]['revenue'] += revenue

    low_products = [
        (
            name,
            data['quantity'],
            round(data['revenue'], 2)
        )
        for name, data in product_data.items()
        if data['quantity'] < threshold
    ]

    low_products.sort(key=lambda x: x[1])

    return low_products


def load_transactions(file_path):
    transactions = []

    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            parts = line.split(",")

            if len(parts) != 5:
                continue

            transaction_id, product_id, quantity, price, date = parts

            transactions.append({
                "transaction_id": transaction_id,
                "product_id": product_id,
                "quantity": int(quantity),
                "price": float(price),
                "date": date
            })

    return transactions
# Processes raw sales data into analytics-ready format
