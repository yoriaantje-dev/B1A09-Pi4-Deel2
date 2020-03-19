import pyodbc
import os.path


def connect_to_DB():
    print("Creating Database connection...")
    path = os.path.abspath("Muziek.accdb")
    print(path)
    conn_str = (r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
                r"DBQ=C:\\Users\\yoria\\OneDrive - ZuydHogeschool\\HS Zuyd\\B1A09 - Databases\\Summatief\\Pi4 Deel2\\code pi4\\code\\Muziek.accdb")
    connection = pyodbc.connect(conn_str)
    return connection


def print_data(conn):
    cursor = conn.cursor()
    for table in cursor.tables(tableType="TABLE"):
        print(table.table_name)

    table_name = str(input("Table Name? "))
    to_print = "SELECT * from " + table_name
    cursor.execute(to_print)

    for row in cursor.fetchall():
        print(row)


def disconnect_sql(conn):
    conn.close()


if __name__ == "__main__":
    database = connect_to_DB()
    print_data(database)
    disconnect_sql(database)
