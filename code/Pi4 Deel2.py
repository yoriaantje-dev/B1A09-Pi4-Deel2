import pyodbc
import os.path
from exc.opdracht_6_pi4_2 import print_songs_per_album as exc6
from exc.opdracht_7_pi4_2 import print_album_with_song_info as exc7
import exc.database_operations as op

def connect_to_DB():
    print("Creating Database connection...")
    path = os.path.abspath("Muziek.accdb")
    print(path)
    conn_str = (r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
                r"DBQ=C:\\Users\\yoria\\OneDrive - ZuydHogeschool\\HS Zuyd\\B1A09 - Databases\\Summatief\\Pi4 Deel2\\code pi4\\code\\Muziek.accdb")
    connection = pyodbc.connect(conn_str)
    return connection


def run(conn):
    cursor, table = op.select_table(conn)
    op.select_column(cursor, table)


def disconnect_sql(conn):
    conn.close()
    

def auto_select(conn, table_name, column_name):
    crsr = conn.cursor()
    selection = "SELECT * from " + table_name
    crsr.execute(selection)
    
    selection = "SELECT " + column_name + " from " + table_name
    crsr.execute(selection)

    rows_in_column = [row for row in crsr.fetchall()]
    for row in rows_in_column:
        for item in row:
            print(item.ljust(27, ' '), end=" - ")
        print("")


if __name__ == "__main__":
    database = connect_to_DB()
    # opdracht 5:
    print("\n\n=====OPDRACHT 5=====")
    auto_select(database, "dbo_ARTIST", "EchteNaam,ArtiestenNaam,Geslacht")

    # opdracht 6:
    print("\n\n=====OPDRACHT 6=====")
    exc6(database)

    # opdracht 7:
    print("\n\n=====OPDRACHT 7=====")
    exc7(database)

    
    
    disconnect_sql(database)
