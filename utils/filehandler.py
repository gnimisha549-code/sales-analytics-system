def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues
    Returns: list of raw lines (strings)
    """

    encodings = ['utf-8', 'latin-1', 'cp1252']

    for enc in encodings:
        try:
            with open(filename, 'r', encoding=enc) as file:
                lines = file.readlines()

                # Skip header and remove empty lines
                raw_lines = [
                    line.strip()
                    for line in lines[1:]
                    if line.strip()
                ]

                # Ensure 50–100 records only
                if len(raw_lines) < 50:
                    print("Warning: Less than 50 records found.")
                    return raw_lines

                return raw_lines[:80]   # safe, deterministic slice

        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return []

    print("Error: Unable to read file with supported encodings.")
    return []


# PART 2: Parsing raw data into dictionaries

def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries
    """

    transactions = []

    for line in raw_lines:
        parts = line.split('|')

        if len(parts) != 8:
            continue

        try:
            transaction = {
                'TransactionID': parts[0].strip(),
                'Date': parts[1].strip(),
                'ProductID': parts[2].strip(),
                'ProductName': parts[3].replace(',', ' ').strip(),
                'Quantity': int(parts[4].replace(',', '')),
                'UnitPrice': float(parts[5].replace(',', '')),
                'CustomerID': parts[6].strip(),
                'Region': parts[7].strip()
            }

            transactions.append(transaction)

        except ValueError:
            continue

    return transactions


# PART 3: VALIDATION AND FILTERING

def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters
    """

    summary = {
        'total_input': len(transactions),
        'invalid': 0,
        'filtered_by_region': 0,
        'filtered_by_amount': 0,
        'final_count': 0
    }

    valid_stage = []

    # Display available regions
    regions = sorted(set(t['Region'] for t in transactions if t.get('Region')))
    print("Available Regions:", regions)

    # Display transaction amount range
    amounts = [
        t['Quantity'] * t['UnitPrice']
        for t in transactions
        if t['Quantity'] > 0 and t['UnitPrice'] > 0
    ]

    if amounts:
        print(f"Transaction Amount Range: {min(amounts)} to {max(amounts)}")

    # -------- VALIDATION STAGE --------
    for t in transactions:
        if (
            not t.get('TransactionID', '').startswith('T') or
            not t.get('ProductID', '').startswith('P') or
            not t.get('CustomerID', '').startswith('C') or
            t.get('Quantity', 0) <= 0 or
            t.get('UnitPrice', 0) <= 0 or
            not t.get('Region')
        ):
            summary['invalid'] += 1
        else:
            valid_stage.append(t)

    # -------- REGION FILTER --------
    region_stage = []
    for t in valid_stage:
        if region and t['Region'] != region:
            summary['filtered_by_region'] += 1
        else:
            region_stage.append(t)

    # -------- AMOUNT FILTER --------
    final_transactions = []
    for t in region_stage:
        amount = t['Quantity'] * t['UnitPrice']

        if min_amount is not None and amount < min_amount:
            summary['filtered_by_amount'] += 1
        elif max_amount is not None and amount > max_amount:
            summary['filtered_by_amount'] += 1
        else:
            final_transactions.append(t)

    summary['final_count'] = len(final_transactions)

    return final_transactions, summary['invalid'], summary
# Handles file reading and writing for sales analytics
