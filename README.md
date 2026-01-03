Transaction Data Cleaning – Python Assignment
Project Overview

This project cleans and validates transaction data stored in a .txt file with non-UTF encoding.
The goal is to handle encoding issues, clean invalid records based on business rules, and report summary statistics.

The solution is implemented using core Python only (no external libraries), making it easy to run in any environment.

Folder Structure
python_assignment/
│
├── transactions.txt     # Input data file (pipe-separated, non-UTF encoding)
├── clean_data.py        # Python script for data cleaning
└── README.md            # Project documentation

Input File Details (transactions.txt)

File format: .txt

Encoding: Non-UTF (latin-1 / ISO-8859-1)

Delimiter: |

Header included

Sample Format
TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region
T001|2024-12-01|P101|Laptop|2|45000|C001|North
T002|2024-12-01|P102|Mouse,Wireless|5|500|C002|South

Data Cleaning Rules

A record is considered INVALID if any of the following conditions are true:

TransactionID does not start with "T"

CustomerID is missing or empty

Region is missing or empty

Quantity is less than 0

UnitPrice is less than 0

Records that are considered VALID

Product names containing commas (e.g. Mouse,Wireless)

Numbers containing commas (e.g. 1,500)

Quantity equal to 0

Empty lines (these are skipped, not counted as invalid)

Output Requirements

After cleaning, the program prints the following summary:

Total records parsed: 80
Invalid records removed: 8
Valid records after cleaning: 72


(Note: Counts depend on the actual dataset.)

How to Run the Code (Step by Step)
Step 1: Install Python

Ensure Python 3.8 or above is installed.

Check version:

python --version


or

python3 --version

Step 2: Open the Project in VS Code

Open VS Code

Click File → Open Folder

Select the python_assignment folder

Step 3: Open Terminal in VS Code

Step 4: Run the Python Script

In the terminal, execute:

python clean_data.py


If Python 3 is mapped as python3, use:

python3 clean_data.py

How the Code Works (High-Level)

Opens the text file using latin-1 encoding

Skips the header row

Reads the file line by line

Skips empty lines

Splits records using |

Applies validation rules

Cleans numeric fields by removing commas

Counts total, invalid, and valid records

Prints a summary to the console

Technologies Used

Python 3

VS Code

Core Python libraries only (open, string, int, float)

Notes for Evaluation

Quantity equal to 0 is treated as valid

Only negative values are invalid

Empty lines are ignored, not counted as invalid

The solution is rule-based and data-driven

