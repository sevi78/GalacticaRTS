import sqlite3
import json

def main(database_name, table_name):
    # Connect to the SQLite database
    conn = sqlite3.connect(database_name)
    conn.row_factory = sqlite3.Row  # This enables column access by name: row['column_name']
    cur = conn.cursor()

    # Execute a query
    cur.execute(f"SELECT * FROM {table_name}")

    # Fetch all rows from the query
    rows = cur.fetchall()

    # Convert query results to dictionary format
    rows_dict = [dict(row) for row in rows]

    # Write dictionary to JSON file
    with open('planets.json', 'w') as f:
        json.dump(rows_dict, f)

    # Close the connection
    conn.close()


if __name__ == "__main__":
    main("database.db", "planets")