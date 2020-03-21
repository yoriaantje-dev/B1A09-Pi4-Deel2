def set_cursor(conn):
    cursor, table = select_table(conn)
    cursor = select_column(cursor, table)
    return cursor


def select_table(conn):
    # Print all Tables in Database
    cursor = conn.cursor()
    for table in cursor.tables(tableType="TABLE"):
        print(table.table_name)

    #Select Table
    table_name = str(input("\nTable Name? "))
    selection = "SELECT * from " + table_name
    cursor.execute(selection)
    return cursor, table_name
    

def select_column(crsr, table_name):
    # Print all columns in selected Table
    columns_in_selection = [column[0] for column in crsr.description]
    for item in columns_in_selection:
        print(item, end=" - ")

    # Select Column
    print("\n\n")
    column_name = str(input("Column Name(s)? "))      
    selection = "SELECT " + column_name + " from " + table_name
    crsr.execute(selection)
    return crsr
    