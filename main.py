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


