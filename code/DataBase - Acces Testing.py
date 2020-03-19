import pyodbc
import os.path


def connect_to_DB():
    print('Creating Database connection...')
    path = os.getcwd()
    conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};'
                          r'DBQ=' + path + '\MuziekDatabase.accdb;')
    return conn


def print_data(conn):
    cursor = conn.cursor()
    cursor.execute('select * dbo_' + table_name)

    for row in cursor.fetchall():
        print(row)


def disconnect_sql(conn):
    conn.close()


if name == __main__:
    database = connect_to_DB()
    show_destination(database)
    disconnect_sql(database)
