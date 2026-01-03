import os
from datetime import datetime
from collections import defaultdict
import pandas as pd  # Assuming data is DataFrame; adjust if list of dicts

def format_currency(amount):
    return f"₹{amount:,.2f}"

def format_percentage(pct):
    return f"{pct:.2f}%"

def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Assume transactions and enriched_transactions are pandas DataFrames
    # with columns like 'date', 'region', 'product_name', 'quantity', 'amount', 'customer_id', etc.
    # 'enriched_transactions' has additional product details from API
    
    total_records = len(transactions)
    total_revenue = transactions['amount'].sum()
    total_transactions = len(transactions)
    avg_order_value = total_revenue / total_transactions if total_transactions > 0 else 0
    date_range = f"{transactions['date'].min().strftime('%Y-%m-%d')} to {transactions['date'].max().strftime('%Y-%m-%d')}"
    
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(output_file, 'w') as f:
        # 1. HEADER
        f.write("=" * 47 + "\n")
        f.write("         SALES ANALYTICS REPORT\n")
        f.write(f"       Generated: {now}\n")
        f.write(f"       Records Processed: {total_records}\n")
        f.write("=" * 47 + "\n\n")
        
        # 2. OVERALL SUMMARY
        f.write("OVERALL SUMMARY\n")
        f.write("-" * 44 + "\n")
        f.write(f"Total Revenue:        {format_currency(total_revenue)}\n")
        f.write(f"Total Transactions:   {total_transactions}\n")
        f.write(f"Average Order Value:  {format_currency(avg_order_value)}\n")
        f.write(f"Date Range:           {date_range}\n\n")
        
        # 3. REGION-WISE PERFORMANCE
        region_stats = transactions.groupby('region').agg({
            'amount': 'sum',
            'date': 'count'  # transaction count
        }).round(2).reset_index()
        region_stats.columns = ['region', 'sales', 'transactions']
        region_stats['pct'] = (region_stats['sales'] / total_revenue * 100).round(2)
        region_stats = region_stats.sort_values('sales', ascending=False)
        
        f.write("REGION-WISE PERFORMANCE\n")
        f.write("-" * 44 + "\n")
        f.write(f"{'Region':<10} {'Sales':<12} {'% of Total':<10} {'Transactions':<12}\n")
        f.write("-" * 44 + "\n")
        for _, row in region_stats.iterrows():
            f.write(f"{row['region']:<10} {format_currency(row['sales']):<12} {format_percentage(row['pct']):<10} {int(row['transactions']):<12}\n")
        f.write("\n")
        
        # 4. TOP 5 PRODUCTS (from enriched)
        product_stats = enriched_transactions.groupby('product_name').agg({
            'quantity': 'sum',
            'amount': 'sum'
        }).round(2).reset_index()
        product_stats = product_stats.sort_values('amount', ascending=False).head(5)
        product_stats['rank'] = range(1, 6)
        
        f.write("TOP 5 PRODUCTS\n")
        f.write("-" * 44 + "\n")
        f.write(f"{'Rank':<4} {'Product Name':<20} {'Qty Sold':<10} {'Revenue':<12}\n")
        f.write("-" * 44 + "\n")
        for _, row in product_stats.iterrows():
            f.write(f"{int(row['rank']):<4} {str(row['product_name'])[:19]:<20} {int(row['quantity']):<10} {format_currency(row['amount']):<12}\n")
        f.write("\n")
        
        # 5. TOP 5 CUSTOMERS
        customer_stats = transactions.groupby('customer_id').agg({
            'amount': 'sum',
            'date': 'count'
        }).round(2).reset_index()
        customer_stats.columns = ['customer_id', 'total_spent', 'order_count']
        customer_stats = customer_stats.sort_values('total_spent', ascending=False).head(5)
        customer_stats['rank'] = range(1, 6)
        
        f.write("TOP 5 CUSTOMERS\n")
        f.write("-" * 44 + "\n")
        f.write(f"{'Rank':<4} {'Customer ID':<12} {'Total Spent':<12} {'Order Count':<12}\n")
        f.write("-" * 44 + "\n")
        for _, row in customer_stats.iterrows():
            f.write(f"{int(row['rank']):<4} {str(row['customer_id'])[:11]:<12} {format_currency(row['total_spent']):<12} {int(row['order_count']):<12}\n")
        f.write("\n")
        
        # 6. DAILY SALES TREND
        daily_stats = transactions.groupby('date').agg({
            'amount': 'sum',
            'customer_id': 'nunique'  # unique customers
        }).round(2).reset_index()
        daily_stats.columns = ['date', 'revenue', 'transactions', 'unique_customers']
        daily_stats['transactions'] = daily_stats['date'].count()  # fix if needed
        
        f.write("DAILY SALES TREND\n")
        f.write("-" * 44 + "\n")
        f.write(f"{'Date':<12} {'Revenue':<12} {'Transactions':<12} {'Unique Cust':<12}\n")
        f.write("-" * 44 + "\n")
        for _, row in daily_stats.iterrows():
            f.write(f"{row['date'].strftime('%Y-%m-%d'):<12} {format_currency(row['revenue']):<12} {int(row['transactions']):<12} {int(row['unique_customers']):<12}\n")
        f.write("\n")
        
        # 7. PRODUCT PERFORMANCE ANALYSIS
        best_day = transactions.loc[transactions.groupby('date')['amount'].idxmax()]['date'].iloc[0].strftime('%Y-%m-%d')
        low_products = enriched_transactions[enriched_transactions['quantity'] < 5]['product_name'].unique() if len(enriched_transactions) > 0 else []
        region_avg = transactions.groupby('region')['amount'].mean().round(2)
        
        f.write("PRODUCT PERFORMANCE ANALYSIS\n")
        f.write("-" * 44 + "\n")
        f.write(f"Best selling day:     {best_day}\n")
        f.write(f"Low performing products: {', '.join(low_products[:3]) if low_products else 'None'}\n")
        f.write("Avg transaction value per region:\n")
        for region, avg in region_avg.items():
            f.write(f"  {region}: {format_currency(avg)}\n")
        f.write("\n")
        
        # 8. API ENRICHMENT SUMMARY
        total_products = enriched_transactions['product_name'].nunique()
        enriched_count = len(enriched_transactions)
        success_rate = (enriched_count / total_records * 100) if total_records > 0 else 0
        unenriched = transactions[~transactions['transaction_id'].isin(enriched_transactions['transaction_id'])]['product_name'].unique()
        
        f.write("API ENRICHMENT SUMMARY\n")
        f.write("-" * 44 + "\n")
        f.write(f"Total products enriched: {total_products}\n")
        f.write(f"Success rate:           {format_percentage(success_rate)}\n")
        f.write(f"Products not enriched:   {', '.join(unenriched[:5]) if unenriched.size > 0 else 'None'}\n")

print("Report generated successfully! Check output/sales_report.txt")
