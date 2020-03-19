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


def run(conn):
    cursor = conn.cursor()
    for table in cursor.tables(tableType="TABLE"):
        print(table.table_name)

    #Select Table
    print("")
    table_name = str(input("Table Name? "))
    selection = "SELECT * from " + table_name
    cursor.execute(selection)
    
    # Print all columns in selected Table
    columns_in_selection = [column[0] for column in cursor.description]
    for item in columns_in_selection:
        print(item, end=" - ")
    
    # Select Column
    print("")
    column_name = str(input("Column Name? "))      
    selection = "SELECT " + column_name + " from " + table_name
    cursor.execute(selection)
    
    # Print all rows in selected Column
    rows_in_column = [row for row in cursor.fetchall()]
    for item in rows_in_column:
        print(item)


def disconnect_sql(conn):
    conn.close()
    
    
if __name__ == "__main__":
    database = connect_to_DB()
    run(database)
    disconnect_sql(database)

