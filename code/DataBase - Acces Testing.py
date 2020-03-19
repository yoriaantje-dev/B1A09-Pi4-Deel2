import pyodbc
import os.path


def connect_to_DB():
    print("Creating Database connection...")
    path = os.getcwd()
    conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
                          r"DBQ=" + path + "\MuziekDatabase.accdb;")
    return conn


def print_data(conn):
    cursor = conn.cursor()
    for table in cursor.tables(tableType='TABLE'):
        print(table.table_name.rstrip())

    table_name = str(input("Table Name? ")).upper()
    cursor.execute("SELECT dbo_" + table_name)

    for row in cursor.fetchall():
        print(row)


def disconnect_sql(conn):
    conn.close()


if __name__ == "__main__":
    database = connect_to_DB()
    print_data(database)
    disconnect_sql(database)
