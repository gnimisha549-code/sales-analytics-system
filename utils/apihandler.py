# Handles API calls (e.g., external services) for the sales analytics system
import requests
import os

def fetch_all_products():
    """
    Fetches all products from DummyJSON API
    """
    url = "https://dummyjson.com/products?limit=100"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        products = data.get("products", [])

        cleaned_products = []

        for p in products:
            cleaned_products.append({
                'id': p.get('id'),
                'title': p.get('title'),
                'category': p.get('category'),
                'brand': p.get('brand'),
                'price': p.get('price'),
                'rating': p.get('rating')
            })

        print(f"Successfully fetched {len(cleaned_products)} products from API")
        return cleaned_products

    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return []
    


    # Create Product mapping

def create_product_mapping(api_products):
    """
    Creates mapping of product ID to product info
    """
    product_mapping = {}

    for product in api_products:
        product_id = product.get('id')

        if product_id is not None:
            product_mapping[product_id] = {
                'title': product.get('title'),
                'category': product.get('category'),
                'brand': product.get('brand'),
                'rating': product.get('rating')
            }

    return product_mapping

    
# Enrich sales data
 
def extract_numeric_product_id(product_id):
    try:
        return int(product_id.replace('P', ''))
    except:
        return None
    
def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information
    """
    enriched_transactions = []

    for t in transactions:
        enriched = t.copy()

        numeric_id = extract_numeric_product_id(t.get('ProductID'))
        api_product = product_mapping.get(numeric_id)

        if api_product:
            enriched['API_Category'] = api_product.get('category')
            enriched['API_Brand'] = api_product.get('brand')
            enriched['API_Rating'] = api_product.get('rating')
            enriched['API_Match'] = True
        else:
            enriched['API_Category'] = None
            enriched['API_Brand'] = None
            enriched['API_Rating'] = None
            enriched['API_Match'] = False

        enriched_transactions.append(enriched)

    save_enriched_data(enriched_transactions)

    return enriched_transactions

# Save enriched data

def save_enriched_data(enriched_transactions, filename='data/enriched_sales_data.txt'):
    """
    Saves enriched transactions back to file
    """
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    header = [
        'TransactionID', 'Date', 'ProductID', 'ProductName',
        'Quantity', 'UnitPrice', 'CustomerID', 'Region',
        'API_Category', 'API_Brand', 'API_Rating', 'API_Match'
    ]

    with open(filename, 'w', encoding='utf-8') as f:
        f.write('|'.join(header) + '\n')

        for t in enriched_transactions:
            row = [
                str(t.get(col)) if t.get(col) is not None else ''
                for col in header
            ]
            f.write('|'.join(row) + '\n')

    print(f"Enriched data saved to {filename}")





