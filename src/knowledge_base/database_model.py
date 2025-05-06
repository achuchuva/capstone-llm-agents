import sqlite3
import json


def run_database_query(query: str, database_path: str = "database/chinook.db") -> str:
    """
    Connect to SQLite database and run a specified query.
    Fetch the results and convert them to a JSON string.
    TODO: Transfer this functionality to an actual AG2 agent.

    Args:
        query (str): The SQL query to execute.
        database_path (str): The path to the SQLite database file.

    Returns:
        str: JSON string representing the query results.
    """

    # Connect to SQLite database via relative path
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Execute a query
    cursor.execute(query)

    # Fetch column names
    columns = [description[0] for description in cursor.description]

    # Fetch all rows and convert to list of dicts
    rows = cursor.fetchall()
    data = [dict(zip(columns, row)) for row in rows]

    # Set the data to a variable in JSON format
    json_result = json.dumps(data, indent=2)

    # Close the connection
    conn.close()

    return json_result


def clean_sql_string(raw_sql: str) -> str:
    """
    Clean the SQL string by removing code block backticks if present.
    """

    # Remove code block backticks if present
    cleaned = raw_sql.strip()
    if cleaned.startswith("```sql"):
        cleaned = cleaned[6:].strip()
    if cleaned.startswith("```"):
        cleaned = cleaned[3:].strip()
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3].strip()
    return cleaned
