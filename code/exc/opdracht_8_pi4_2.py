import pyodbc
import os.path

def connect_to_DB():
    print("Creating Database connection...")
    conn_str = (r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
                r"DBQ=C:\\Users\\yoria\\OneDrive - ZuydHogeschool\\HS Zuyd\\B1A09 - Databases\\Summatief\\Pi4 Deel2\\code pi4\\code\\Muziek.accdb")
    connection = pyodbc.connect(conn_str)
    return connection


def print_artist_from_last_name(conn):
    # Fetch all Artists and Names
    print("The following artists are found in de provided database:")
    table_cursor = conn.cursor()
    #ARTIST (selection)
    for table in table_cursor.tables(tableType="TABLE"):
        if table.table_name == "dbo_ARTIST":
            print("\n>>> SYSTEM \n    ===FOUND TABLE dbo_ARTIST===")
            crsr = conn.cursor()
            crsr.execute("SELECT ArtistID,EchteNaam,RolID from dbo_ARTIST")
            
            values = crsr.fetchall()
            print("The following artists are found in de provided database:")
            for row in values:
                print_num = (str(row[0])+".").ljust(3, ' ')
                artist_name = row[1].split(" ")
                if len(artist_name) == 2:
                    print(f"{print_num} Artist {artist_name[1]}, {artist_name[0]}")
                else:
                    artist_name.insert(0, [])
                    for name in range(2, len(artist_name)):
                        artist_name[0].append(artist_name[name])
                    print(f"{print_num} Artist", end="")
                    for name in artist_name[0]:
                        print(f" {name}",end="")
                    print(f", {artist_name[1]}")
            artist_id = int(input("Please select an artist based on their number: ")) - 1
            artist_dict = {"id": values[artist_id][0],
					       "name": values[artist_id][1],
					       "rol_id": values[artist_id][2]
                          }
            del crsr
    #ROL
    for table in table_cursor.tables(tableType="TABLE"):
        if table.table_name == "dbo_ROL":
            print("\n>>> SYSTEM \n    ===FOUND TABLE dbo_ROL===")
            crsr = conn.cursor()
            crsr.execute("SELECT * from dbo_ROL")

            values = crsr.fetchall()
            for row in values:
                if row[0] == artist_dict["rol_id"]:
                    artist_dict["rol_id"] = row[1]
            if type(artist_dict["rol_id"]) != type("str"):
                artist_dict["rol_id"] = "Error"

            print(artist_dict)
    
    #BANDARTIST
    for table in table_cursor.tables(tableType="TABLE"):
        if table.table_name == "dbo_BANDARTIST":
            print("\n>>> SYSTEM \n    ===FOUND TABLE dbo_BANDARTIST===")
            crsr = conn.cursor()
            crsr.execute("SELECT * from dbo_BANDARTIST")

            values = crsr.fetchall()
            #Get BandID
            for row in values:
                if row[1] == artist_dict["id"]:
                    artist_dict["band_id"] = row[0]
            if "band_id" not in artist_dict.keys():
                artist_dict["band_id"] = "Error"
            #Get BandMembers
            else:
                member_list = []
                for row in values:
                    if row[0] == artist_dict["band_id"]:
                        member_list.append(row[1])
                artist_dict["band_members"] = member_list
    #BAND
    for table in table_cursor.tables(tableType="TABLE"):
        if table.table_name == "dbo_BAND":
            print("\n>>> SYSTEM \n    ===FOUND TABLE dbo_BAND===")
            crsr = conn.cursor()
            crsr.execute("SELECT * from dbo_BAND")

            values = crsr.fetchall()
            if artist_dict["band_id"] == "Error":
                artist_dict["band_info"] = "Error"
            else:
                for row in values:
                    if row[0] == artist_dict["band_id"]:
                        artist_dict["band_info"] = {"name": row[1], "country": row[2]}
    #ARTIST (fetch band members)
    for table in table_cursor.tables(tableType="TABLE"):
        if table.table_name == "dbo_ARTIST":
            print("\n>>> SYSTEM \n    ===FOUND TABLE dbo_ARTIST===")
            crsr = conn.cursor()
            crsr.execute("SELECT ArtistID,EchteNaam,Artiestennaam from dbo_ARTIST")
            
            values = crsr.fetchall()
            if "band_members" not in artist_dict.keys():
                pass
            else:
                for row in values:
                    for num in range(len(artist_dict["band_members"])):
                        num -= 1
                        if row[0] == artist_dict["band_members"][num]:
                            member_info = row[2] + " (" + row[1] + ")"
                            artist_dict["band_members"].append(member_info)
                            artist_dict["band_members"].remove(row[0])

    #ARTISTSONG
    for table in table_cursor.tables(tableType="TABLE"):
        if table.table_name == "dbo_SONGARTIST":
            print("\n>>> SYSTEM \n    ===FOUND TABLE dbo_SONGARTIST===")
            crsr = conn.cursor()
            crsr.execute("SELECT * from dbo_SONGARTIST")

            values = crsr.fetchall()
            song_list = []
            for row in values:
                if row[1] == artist_dict["id"]:
                    song_list.append(row[0])
                artist_dict["songs"] = song_list
                if "songs" not in artist_dict.keys():
                    artist_dict["songs"] = "Error" 
    #SONG
    for table in table_cursor.tables(tableType="TABLE"):
        if table.table_name == "dbo_SONG":
            print("\n>>> SYSTEM \n    ===FOUND TABLE dbo_SONG===")
            crsr = conn.cursor()
            crsr.execute("SELECT SongID,Titel from dbo_SONG")

            values = crsr.fetchall()
            if artist_dict["songs"] == "Error":
                pass
            else:
                for row in values:
                    for num in range(len(artist_dict["songs"])):
                        num -= 1
                        if row[0] == artist_dict["songs"][num]:
                            artist_dict["songs"].append(row[1])
                            artist_dict["songs"].remove(row[0])


    print(f"Artiest {artist_dict['name']} speelt als {artist_dict['rol_id']} in de volgende band:")
    print(f"Bandnaam: {artist_dict['band_info']['name']}, uit {artist_dict['band_info']['country']}")
    print(f"Bandleden:")
    for member in artist_dict['band_members']:
        print(" -", member)
    print("\nDe artiest heeft volgende nummers geschreven:")
    for song in artist_dict['songs']:
        print(" -", song)



if __name__ == "__main__":
    # opdracht 8:
    print("\n\n=====OPDRACHT 8=====")
    database = connect_to_DB()
    print_artist_from_last_name(database)