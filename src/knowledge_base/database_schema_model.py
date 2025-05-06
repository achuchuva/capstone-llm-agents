import sqlite3
import json


def get_database_schema(database_path: str = "database/chinook.db") -> str:
    """
    Connect to SQLite database and retrieve the schema of all user-defined tables.
    Convert the schema to a JSON string.
    TODO: Transfer this functionality to an actual AG2 agent.

    Args:
        datebase_path (str): The path to the SQLite database file.

    Returns:
        str: JSON string representing the database schema.
    """
    # Connect to SQLite database
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Get all user-defined tables
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
    )
    tables = [row[0] for row in cursor.fetchall()]

    # Build simplified schema dictionary
    schema = {}

    for table in tables:
        cursor.execute(f"PRAGMA table_info({table})")
        columns_info = cursor.fetchall()

        # Extract just the column names
        schema[table] = [col[1] for col in columns_info]

    # Convert schema to JSON string without outer braces
    schema_items = [
        f'"{table}": {json.dumps(columns, indent=2)}'
        for table, columns in schema.items()
    ]
    schema_json_without_braces = ",\n".join(schema_items)

    # Close connection
    conn.close()

    return schema_json_without_braces


database_simplified_schema_kb = """
"Album": [
  "AlbumId",
  "Title",
  "ArtistId"
],
"Customer": [
  "CustomerId",
  "FirstName",
  "LastName",
  "Company",
  "Address",
  "City",
  "State",
  "Country",
  "PostalCode",
  "Phone",
  "Fax",
  "Email",
  "SupportRepId"
],
"""


def get_database_table_schema(database_path: str = "database/chinook.db") -> str:
    """
    Connect to SQLite database and retrieve the schema (just names) of all user-defined tables.
    Convert the schema to a JSON string.
    TODO: Transfer this functionality to an actual AG2 agent.

    Args:
        datebase_path (str): The path to the SQLite database file.

    Returns:
        str: JSON string representing the database tables.
    """
    # Connect to SQLite database
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Get all user-defined tables
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
    )
    tables = [row[0] for row in cursor.fetchall()]

    # Convert table list to JSON-formatted string
    tables_json = json.dumps(tables, indent=2)

    # Close connection
    conn.close()

    return tables_json
