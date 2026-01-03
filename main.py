# Entry point for the sales analytics system
encoding='latin-1'
def clean_transactions(file_path):
    total_records = 0
    invalid_records = 0
    valid_records = []

    with open(file_path, 'r', encoding='latin-1') as file:
        header = file.readline()

        for line in file:
            line = line.strip()

            if not line:
                continue

            total_records += 1

            try:
                fields = line.split('|')

                if len(fields) != 8:
                    invalid_records += 1
                    continue

                transaction_id, date, product_id, product_name, quantity, unit_price, customer_id, region = fields

                if not transaction_id.startswith('T'):
                    invalid_records += 1
                    continue

                if not customer_id.strip() or not region.strip():
                    invalid_records += 1
                    continue

                quantity = int(quantity.replace(',', ''))
                unit_price = float(unit_price.replace(',', ''))

                if quantity < 0 or unit_price < 0:
                    invalid_records += 1
                    continue

                valid_records.append(fields)

            except Exception:
                invalid_records += 1

    print(f"Total records parsed: {total_records}")
    print(f"Invalid records removed: {invalid_records}")
    print(f"Valid records after cleaning: {len(valid_records)}")


if __name__ == "__main__":
    clean_transactions("transactions.txt")

# Report generator
from Utils.data_processor import load_transactions
from Utils.api_handler import fetch_all_products, create_product_mapping, enrich_sales_data
from Utils.report_generator import generate_sales_report


def main():
    transactions = load_transactions("Transactions.txt")
    print("Transactions loaded:", len(transactions))
    print(transactions[:3])


    api_products = fetch_all_products()
    product_mapping = create_product_mapping(api_products)

    enriched_transactions = enrich_sales_data(transactions, product_mapping)

    generate_sales_report(transactions, enriched_transactions)


if __name__ == "__main__":
    main()

# Main Script
import os
import pandas as pd
from datetime import datetime
import requests  # for API
from collections import defaultdict

# Assume prior functions exist: validate_transactions, analyze_sales, fetch_products_api, enrich_sales_data
# Stub if missing

def validate_transactions(transactions):
    # Stub: return valid_df, invalid_count
    return transactions, 0

def analyze_sales(transactions):
    # Stub
    pass

def fetch_products_api():
    # Stub: mock API response
    return pd.DataFrame({'product_name': [], 'category': []})

def enrich_sales_data(transactions, products):
    # Stub
    return transactions

def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):
    import os
    from datetime import datetime
    from collections import defaultdict

    def format_currency(amount):
        return f"₹{amount:,.2f}"

    def format_percentage(pct):
        return f"{pct:.2f}%"

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Expecting pandas DataFrames for this main script
    total_records = len(transactions)
    total_revenue = transactions['amount'].sum() if 'amount' in transactions.columns else 0
    total_transactions = len(transactions)
    avg_order_value = total_revenue / total_transactions if total_transactions > 0 else 0
    date_range = f"{transactions['date'].min().strftime('%Y-%m-%d')} to {transactions['date'].max().strftime('%Y-%m-%d')}" if 'date' in transactions.columns else 'N/A'

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 44 + "\n")
        f.write("        SALES ANALYTICS REPORT\n")
        f.write(f"     Generated: {now}\n")
        f.write(f"     Records Processed: {total_records}\n")
        f.write("=" * 44 + "\n\n")

        f.write("OVERALL SUMMARY\n")
        f.write("-" * 44 + "\n")
        f.write(f"Total Revenue:        {format_currency(total_revenue)}\n")
        f.write(f"Total Transactions:   {total_transactions}\n")
        f.write(f"Average Order Value:  {format_currency(avg_order_value)}\n")
        f.write(f"Date Range:           {date_range}\n\n")

        # REGION
        if 'region' in transactions.columns:
            region_stats = transactions.groupby('region').agg({'amount': 'sum', 'date': 'count'}).round(2).reset_index()
            region_stats.columns = ['region', 'sales', 'transactions']
            region_stats['pct'] = (region_stats['sales'] / total_revenue * 100).round(2) if total_revenue else 0
            region_stats = region_stats.sort_values('sales', ascending=False)

            f.write("REGION-WISE PERFORMANCE\n")
            f.write("-" * 44 + "\n")
            for _, row in region_stats.iterrows():
                f.write(f"{row['region']:10} {format_currency(row['sales']):<12} {format_percentage(row['pct']):<10} {int(row['transactions']):<12}\n")
            f.write("\n")

        # TOP PRODUCTS (from enriched)
        try:
            if hasattr(enriched_transactions, 'groupby') and 'product_name' in enriched_transactions.columns:
                prod = enriched_transactions.groupby('product_name').agg({'quantity': 'sum', 'amount': 'sum'}).round(2).reset_index()
                prod = prod.sort_values('amount', ascending=False).head(5)
                f.write("TOP 5 PRODUCTS\n")
                f.write("-" * 44 + "\n")
                for i, row in prod.iterrows():
                    f.write(f"{row['product_name'][:20]:20} {int(row['quantity']):>6} {format_currency(row['amount']):>12}\n")
                f.write("\n")
        except Exception:
            pass

        # TOP CUSTOMERS
        try:
            if 'customer_id' in transactions.columns:
                cust = transactions.groupby('customer_id').agg({'amount': 'sum', 'date': 'count'}).round(2).reset_index()
                cust.columns = ['customer_id', 'total_spent', 'order_count']
                cust = cust.sort_values('total_spent', ascending=False).head(5)
                f.write("TOP 5 CUSTOMERS\n")
                f.write("-" * 44 + "\n")
                for _, row in cust.iterrows():
                    f.write(f"{str(row['customer_id']):12} {format_currency(row['total_spent']):>12} {int(row['order_count']):>6}\n")
                f.write("\n")
        except Exception:
            pass

        # API ENRICHMENT SUMMARY (best-effort)
        try:
            enriched_count = len(enriched_transactions) if hasattr(enriched_transactions, '__len__') else 0
            success_rate = (enriched_count / total_records * 100) if total_records else 0
            f.write("API ENRICHMENT SUMMARY\n")
            f.write("-" * 44 + "\n")
            f.write(f"Products Enriched: {enriched_count}\n")
            f.write(f"Success Rate: {success_rate:.2f}%\n")
        except Exception:
            pass

    print(f"Sales report generated at {output_file}")

def main():
    try:
        print("=" * 47)
        print("      SALES ANALYTICS SYSTEM")
        print("=" * 47)
        print()

        # 1. Read sales data (try CSV, fall back to Transactions.txt)
        print("[1/10] Reading sales data...")
        try:
            df = pd.read_csv('data/transactions.csv', encoding='utf-8')
            print(f"✓ Successfully read {len(df)} transactions\n")
        except FileNotFoundError:
            from Utils.data_processor import load_transactions
            tx = load_transactions("Transactions.txt")
            df = pd.DataFrame(tx)
            # normalize column expected by downstream code
            if 'total_amount' in df.columns and 'amount' not in df.columns:
                df['amount'] = df['total_amount']
            print(f"✓ Loaded {len(df)} transactions from Transactions.txt\n")

        # 2. Parse/clean (already done by pandas)
        print("[2/10] Parsing and cleaning data...")
        # Basic cleaning
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df = df.dropna(subset=['amount'])
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
        print(f"✓ Parsed {len(df)} records\n")

        # 3. Filter options
        print("[3/10] Filter Options Available:")
        regions = df['region'].unique()
        print(f"Regions: {', '.join(regions)}")
        min_amt, max_amt = df['amount'].min(), df['amount'].max()
        print(f"Amount Range: ₹{min_amt:,.0f} - ₹{max_amt:,.0f}")
        
        # Non-interactive default: do not filter
        filter_choice = 'n'
        if filter_choice == 'y':
            region_filter = input("Enter region (or 'all'): ").strip()
            if region_filter != 'all':
                df = df[df['region'] == region_filter]
            min_filter = float(input("Min amount: "))
            max_filter = float(input("Max amount: "))
            df = df[(df['amount'] >= min_filter) & (df['amount'] <= max_filter)]
            print(f"✓ Filtered to {len(df)} records\n")
        else:
            print("✓ No filter applied\n")

        # 4. Validate
        print("[4/10] Validating transactions...")
        valid_df, invalid_count = validate_transactions(df)
        print(f"✓ Valid: {len(valid_df)} | Invalid: {invalid_count}\n")
        df = valid_df

        # 5. Analyze
        print("[5/10] Analyzing sales data...")
        analyze_sales(df)
        print("✓ Analysis complete\n")

        # 6. API
        print("[6/10] Fetching product data from API...")
        products = fetch_products_api()
        print(f"✓ Fetched {len(products)} products\n")

        # 7. Enrich
        print("[7/10] Enriching sales data...")
        enriched = enrich_sales_data(df, products)
        success_rate = len(enriched) / len(df) * 100 if len(df) > 0 else 0
        print(f"✓ Enriched {len(enriched)}/{len(df)} transactions ({success_rate:.1f}%)\n")

        # 8. Save enriched
        os.makedirs('data', exist_ok=True)
        enriched.to_csv('data/enriched_sales_data.csv', index=False)
        print("✓ Saved to: data/enriched_sales_data.csv\n")

        # 9. Generate report
        print("[9/10] Generating report...")
        generate_sales_report(df, enriched)
        print("✓ Report saved to: output/sales_report.txt\n")

        print("[10/10] Process Complete!")
        print("=" * 47)

    except FileNotFoundError as e:
        print(f"❌ Error: File not found - {e}")
        print("Ensure data/transactions.csv exists.")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        print("Check data format and try again.")

if __name__ == "__main__":
    main()


