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
    corsor, table = select_table(conn)
    select_column(corsor, table)


def disconnect_sql(conn):
    conn.close()
    

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
    
    # Print all rows in selected Column(s)
    rows_in_column = [row for row in crsr.fetchall()]
    for item in rows_in_column:
        print(* item, sep=",")
    

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


def print_songs_per_album(conn):
    album_dict = {}
    table_cursor = conn.cursor()
    for table in table_cursor.tables(tableType="TABLE"):
        if table.table_name == "dbo_ALBUM":
            print("\n>>> SYSTEM \n    ===FOUND TABLE ALBUM===")
            crsr = conn.cursor()
            crsr.execute("SELECT AlbumID,Naam,TypeID from dbo_ALBUM")
            
            values = crsr.fetchall()
            for album in values:
                album_id, album_naam, album_typeid = album[0], album[1], album[2]           
                album_dict.update({album_naam: {"id": album_id,
                                        "type": album_typeid,
                                        "song_list": []
                                        }})
            del crsr

        elif table.table_name == "dbo_ALBUMSONG":
            print("\n>>> SYSTEM \n    ===FOUND TABLE ALBUMSONG===")
            crsr = conn.cursor()
            crsr.execute("SELECT * from dbo_ALBUMSONG")

            values = crsr.fetchall()
            for link in values:
                for a_name, a_values in album_dict.items():
                        if a_values["id"] == link[1]:
                            a_values["song_list"].append(link[0])
            del crsr

        elif table.table_name == "dbo_ALBUMTYPE":
            print("\n>>> SYSTEM \n    ===FOUND TABLE ALBUMTYPE===")
            crsr = conn.cursor()
            crsr.execute("SELECT * from dbo_ALBUMTYPE")

            values = crsr.fetchall()
            for link in values:
                for a_name, a_values in album_dict.items():
                    if link[0] == a_values["type"]:
                        a_values["type"] = link[1]

            del crsr
        
        elif table.table_name == "dbo_SONG":
            print("\n>>> SYSTEM \n    ===FOUND TABLE SONG===")
            crsr = conn.cursor()
            crsr.execute("SELECT SongID,Titel from dbo_SONG")

            values = crsr.fetchall()
            for song in values:
                song_id, song_name = song[0], song[1]

                for a_name, a_values in album_dict.items():
                    for stored_song_id in a_values["song_list"]:
                        if song_id == stored_song_id:
                            a_values["song_list"].append(song_name)
                            a_values["song_list"].remove(song_id)
            del crsr

    out = 1
    for a_name, a_values in album_dict.items():
        print(f"\n\n>>> OUTPUT NUMBER {out}")
        print(f"Het album {a_name} is van het genre: {a_values['type']}"
                f"\nMet de liedjes:")
        num = 1
        for song in a_values["song_list"]:
            print(f"{num}. {song}")
            num += 1
        out += 1


if __name__ == "__main__":
    database = connect_to_DB()
    # opdracht 5:
    print("\n\n=====OPDRACHT 5=====")
    auto_select(database, "dbo_ARTIST", "EchteNaam,ArtiestenNaam,Geslacht")

    # opdracht 6:
    print("\n\n=====OPDRACHT 6=====")
    print_songs_per_album(database)

    # opdracht 7:
    print("\n\n=====OPDRACHT 7=====")
    print_songs_per_album(database)
    
    
    disconnect_sql(database)
