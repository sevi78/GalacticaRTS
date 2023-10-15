import os
import sqlite3
from sqlite3 import Error

from tabulate import tabulate


def get_database_file_path(**kwargs):
    filename = kwargs.get("filename", None)

    if not filename:
        filename = "database"

    dirpath = os.path.dirname(os.path.realpath(__file__))
    database_path = os.path.split(dirpath)[0].split("source")[0] + "database" + os.sep
    database_file_path = database_path + filename + ".db"
    return database_file_path


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print("create_connection: error: ", e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        conn.commit()
    except Error as e:
        print("create_table error:", e)


def insert(conn, insert_sql):
    try:
        c = conn.cursor()
        c.execute(insert_sql)
    except Error as e:
        print("insert error: ", e)


def select(conn, sql):
    cur = conn.cursor()
    cur.execute(sql)

    rows = cur.fetchall()

    for row in rows:
        print("database_access.select:", row)

    return rows


def select_all(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM planets")

    rows = cur.fetchall()
    print("select * from planets: ", rows)
    for row in rows:
        print("database_access.select_all:", rows)

    return rows


def get_dict_from_database(id):
    conn = create_connection(get_database_file_path())
    cur = conn.cursor()

    # execute the SELECT statement
    select_sql = f"SELECT * FROM planets WHERE id = '{id}'"
    cur.execute(select_sql)

    # fetch the first row as a tuple
    row = cur.fetchone()

    # convert the tuple to a dictionary
    keys = [description[0] for description in cur.description]
    values = list(row)
    result_dict = dict(zip(keys, values))

    # close the cursor and connection
    cur.close()
    conn.close()
    return result_dict


def get_position_from_db(filename, id):
    conn = create_connection(get_database_file_path(filename=filename))
    cur = conn.cursor()
    cur.execute(f"select x, y from planets where id = {id}")
    row = cur.fetchall()
    conn.close()
    return row


def save_obj__(filename, tablename, obj):
    conn = create_connection(filename)
    cur = conn.cursor()

    # Check if the table exists
    cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tablename}'")
    table_exists = cur.fetchone()
    variables = obj.get_interface_variables()

    # Create the new table if it doesn't exist
    if not table_exists:
        columns = ', '.join([f"{key.lower()} REAL NOT NULL" for key in variables])
        create_table_sql = f"""CREATE TABLE {tablename} (
                                    id INTEGER PRIMARY KEY,
                                    name TEXT NOT NULL,
                                    {columns}
                                );"""
        cur.execute(create_table_sql)

    # Insert data from obj.get_interface_variables()
    data = {key.lower(): getattr(obj, key) for key in variables}
    columns = ', '.join(data.keys())
    placeholders = ', '.join(['?' for _ in data.values()])
    values = tuple(data.values())

    cur.execute(f"INSERT INTO {tablename} (name, {columns}) VALUES (?, {placeholders})", ('ship_config',) + values)

    conn.commit()
    conn.close()

    """this resutls to error: cur.execute(f"INSERT INTO {tablename} (name, {columns}) VALUES (?, {placeholders})", ('ship_config',) + values)
    sqlite3.OperationalError: table ship_config has no column named food, fix it!!!"""


def save_obj__(filename, tablename, obj):
    conn = create_connection(filename)
    cur = conn.cursor()

    # Check if the table exists
    cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tablename}'")
    table_exists = cur.fetchone()
    variables = obj.get_interface_variables()

    # Create the new table if it doesn't exist
    if not table_exists:
        columns = ', '.join([f"{key.lower()} REAL NOT NULL" for key in variables])
        create_table_sql = f"""CREATE TABLE {tablename} (
                                    id INTEGER PRIMARY KEY,
                                    name TEXT NOT NULL,
                                    {columns}
                                );"""
        cur.execute(create_table_sql)

    conn.commit()
    conn.close()

    print_ship_config_table(filename, tablename)
    return
    # Insert data from obj.get_interface_variables()
    data = {key.lower(): getattr(obj, key) for key in variables}
    columns = ', '.join(data.keys())
    placeholders = ', '.join(['?' for _ in data.values()])
    values = tuple(data.values())

    cur.execute(f"INSERT INTO {tablename} (name, {columns}) VALUES (?, {placeholders})", ('ship_config',) + values)

    conn.commit()
    conn.close()


def create_ship_table(filename, obj):
    conn = create_connection(filename)
    cur = conn.cursor()

    # Create the new table if it doesn't exist
    variables = obj.get_interface_variables()
    columns = ', '.join([f"{key.lower()} REAL NOT NULL" for key in variables])
    create_table_sql = f"""CREATE TABLE IF NOT EXISTS ship_config (
                                id INTEGER PRIMARY KEY,
                                name TEXT NOT NULL,
                                {columns}
                            );"""
    cur.execute(create_table_sql)

    conn.commit()
    conn.close()


def save_obj(filename, tablename, obj):
    conn = create_connection(filename)
    cur = conn.cursor()

    # Check if the table exists
    cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tablename}'")
    table_exists = cur.fetchone()

    variables = obj.get_interface_variables()
    # Create the new table if it doesn't exist
    # if not table_exists:
    create_ship_table(filename, obj)
    print_ship_config_table(filename, tablename)

    return

    # Insert data from obj.get_interface_variables()
    data = {key.lower(): getattr(obj, key) for key in variables}
    columns = ', '.join(data.keys())
    placeholders = ', '.join(['?' for _ in data.values()])
    values = tuple([tablename] + list(data.values()))

    cur.execute(f"INSERT INTO {tablename} (name, {columns}) VALUES ({placeholders})", values)

    conn.commit()
    conn.close()


def print_ship_config_table(filename, tablename):
    conn = create_connection(filename)
    cur = conn.cursor()

    # Retrieve data from the table
    cur.execute(f"SELECT * FROM {tablename}")
    data = cur.fetchall()

    # Retrieve column names
    column_names = [description[0] for description in cur.description]

    # Print the table using tabulate
    print(tabulate(data, headers=column_names, tablefmt='grid'))

    conn.close()


if __name__ == '__main__':

    conn = create_connection(get_database_file_path())
    try:
        pass
        # create_table(conn, create_planet_table_sql)
        # insert_planet(conn)
        # select_all(conn)
        # insert(conn, "ALTER TABLE planets ADD COLUMN orbit_angle INTEGER NOT NULL DEFAULT 0;")
        # insert(conn, "ALTER TABLE planets RENAME COLUMN atmosphere_name TO atmosphere_name;")
        # insert(conn, "UPDATE planets SET atmosphere_name = atmosphere.png WHERE atmosphere_name != ''")
        # insert(conn, "UPDATE planets SET type = 'sun' WHERE name IN ('Sun', 'Sun1')")
        # insert(conn, "UPDATE planets SET info_text = ")
        # insert(conn, "UPDATE planets SET x = 2600 where id == 12")
        # insert(conn, "UPDATE planets SET type = 'planet' where type == ''")
        # conn.commit()
        # create_ship_table("config.db")
        # print_ship_config_table("config.db", "ship_config")
        #insert(conn, "ALTER TABLE planets RENAME COLUMN x TO world_x;")
        #insert(conn, "ALTER TABLE planets RENAME COLUMN y TO world_y;")

        #insert(conn, "ALTER TABLE planets RENAME COLUMN width TO world_width;")
        #insert(conn, "ALTER TABLE planets RENAME COLUMN height TO world_height;")

    except Error as e:
        print("Error:", e)
    finally:
        # select_all(conn)
        conn.close()
        pass
