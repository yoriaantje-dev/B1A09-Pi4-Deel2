import pyodbc
import os.path


def connect_to_DB():
    print('connecting to database...')
    path = os.getcwd()
    conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};'
                          r'DBQ=' + path + '\MuziekDatabase.accdb;')
    return conn


def disconnect_sql(conn):
    conn.close()


def show_destination(conn):
    bestemmingen = conn.cursor()
    SelectString = 'SELECT Plaats, Land, Werelddeel, Bestemmingcode FROM Bestemming;'

    bestemmingen.execute(SelectString)
    bestemmingenList = bestemmingen.fetchall()

    print(len(bestemmingenList), 'bestemmingen : ')

    for bestemming in bestemmingenList:
        print('   ', bestemming.Plaats, bestemming.Land, bestemming.Werelddeel)
    print('')


# ---------------------------- MAIN PROGRAM -----------------------------------------
database = connect_to_DB()
show_destination(database)
disconnect_sql(database)





