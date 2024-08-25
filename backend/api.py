import sqlite3

# List of fields to show in the output
FIELDS_TO_SHOW = []


def filter_data(data, fields_to_show):
    if len(fields_to_show) == 0:
        return [row for row in data]
    return [
        {field: row[field] for field in fields_to_show if field in row} for row in data
    ]


def execute_sqlite_query(database_name, query):
    """
    Executes a SQLite query and returns the result.

    Parameters:
    database_name (str): Name of the SQLite database file.
    query (str): SQL query to execute.

    Returns:
    list: A list of dictionaries containing the query results.
    """
    try:
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()
        cursor.execute(query)
        columns = [description[0] for description in cursor.description]
        results = cursor.fetchall()
        conn.close()
        return [dict(zip(columns, row)) for row in results]
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def join_tables(database_name, table1_name, table2_name, join_field):
    """
    Join two tables in a SQLite database based on a specified join field.

    This function constructs and executes a SQL query to perform an INNER JOIN
    between two tables in the specified database.

    Parameters:
    database_name (str): The name of the SQLite database file.
    table1_name (str): The name of the first table to join.
    table2_name (str): The name of the second table to join.
    join_field (str): The field name to use for joining the tables.

    Returns:
    list: A list of dictionaries, where each dictionary represents a row
          from the joined tables. Returns None if an error occurs during
          query execution.
    """
    query = f"SELECT * FROM {table1_name} JOIN {table2_name} ON {table1_name}.{join_field} = {table2_name}.{join_field}"
    return execute_sqlite_query(database_name, query)


def get_all_data(database_name, table_name):
    query = f"SELECT * FROM {table_name}"
    return execute_sqlite_query(database_name, query)


def get_row_by_id(data, value_to_search, col="ID", fields=None):
    """
    Retrieve specific rows from a list of dictionaries based on a given value_to_search.

    This function searches for rows in the provided data where the specified column
    matches the given value_to_search. It can return either the entire rows or a subset of
    fields from the rows.

    Parameters:
    data (list): A list of dictionaries, where each dictionary represents a row of data.
    value_to_search: The value to match in the specified column for identifying the rows.
    col (str, optional): The key in each dictionary to use for matching the value_to_search.
                         Defaults to 'ID'.
    fields (list, optional): A list of field names to return. If provided, only these
                             fields will be included in the result. Defaults to None,
                             which returns all fields.

    Returns:
    list: A list of dictionaries representing the matching rows. Each dictionary contains
          either all fields or the specified fields. Returns an empty list if no matching
          rows are found.
    """
    print(type(data[0]["ID"]))
    print(type(value_to_search))
    print(f"Searching for ID {value_to_search}")
    print(data[0]["ID"] == value_to_search)
    matching_rows = [row for row in data if str(row[col]) == value_to_search]
    print(f"Found {len(matching_rows)} rows with ID {value_to_search}")
    if fields:
        return [
            {field: row[field] for field in fields if field in row}
            for row in matching_rows
        ]
    else:
        return matching_rows
