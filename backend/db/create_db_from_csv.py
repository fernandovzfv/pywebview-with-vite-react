import csv
import sqlite3
import datetime

# input data for table1
table_schema_table1 = """
CREATE TABLE IF NOT EXISTS table1 (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    CODE INTEGER,
    CATEGORY TEXT,
    DESCRIPTION TEXT
)
"""
cols_type_number_table1 = ['CODE']

# input data for table2
table_schema_table2 = """
CREATE TABLE IF NOT EXISTS table2 (
    ID INTEGER PRIMARY KEY REFERENCES table2(ID),
    ISSUED TEXT,
    COMMENTED TEXT
)
"""


# Use these variables when calling your convert_csv_to_sqlite function
def convert_csv_to_sqlite(csv_file, db_file, table_schema, cols_type_number, cols_type_date, table_name):
    """
    Converts a CSV file to a SQLite database table.

    This function reads data from a CSV file, processes it according to specified column types,
    and inserts the data into a SQLite database table. It handles numeric and date conversions
    for specified columns.

    Parameters:
    csv_file (str): Path to the input CSV file.
    db_file (str): Path to the SQLite database file.
    table_schema (str): SQL schema for creating the table.
    cols_type_number (list): List of column names to be treated as numeric types.
    cols_type_date (list): List of column names to be treated as date types.
    table_name (str): Name of the table to be created in the database.

    Returns:
    None

    Note:
    - The function assumes the CSV file has a header row.
    - Date columns are expected to be in the format 'dd/mm/yyyy'.
    - Invalid or empty date entries are stored as NULL in the database.
    """
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)

        create_table_query = table_schema
        cursor.execute(create_table_query)

        for row in csv_reader:
            processed_row = []
            for i, item in enumerate(row):
                if headers[i] in cols_type_number:
                    processed_row.append(int(item))
                elif headers[i] in cols_type_date:
                    if item and item.strip():  # Check if item is not empty or just whitespace
                        try:
                            date = datetime.datetime.strptime(item, '%d/%m/%Y')
                            processed_row.append(date.strftime('%Y-%m-%d'))
                        except ValueError:
                            processed_row.append(None)  # Append None for invalid date strings
                    else:
                        processed_row.append(None)  # Append None for empty strings
                else:
                    processed_row.append(item)

            placeholders = ','.join(['?' for _ in processed_row])
            insert_query = f"INSERT INTO {table_name} ({','.join(headers)}) VALUES ({placeholders})"
            cursor.execute(insert_query, processed_row)

    conn.commit()
    conn.close()

# Create and populate the SQLite database from the pagag_entregables_ec1.csv file
csv_table1 = 'table1.csv'
db_file = '../../database.db'
convert_csv_to_sqlite(csv_table1,
                      db_file,
                      table_schema_table1,
                      cols_type_number_table1,
                      [],
                      "table1")


# Create and populate the SQLite database from the pagag_revs_ec1.csv file
csv_table2 = 'table2.csv'
convert_csv_to_sqlite(csv_table2,
                      db_file,
                      table_schema_table2,
                      [],
                      [],
                      "table2")
