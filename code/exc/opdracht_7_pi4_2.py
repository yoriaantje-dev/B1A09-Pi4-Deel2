def print_album_with_song_info(conn):
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