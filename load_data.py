import json
import os.path
import sqlite3
from sys import argv


def create_db(sqlitefilename):
    connection = sqlite3.connect(sqlitefilename)
    cursor = connection.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS stations
        (id INTEGER PRIMARY KEY, 
        name TEXT, 
        lat REAL, 
        lon REAL)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS pollutants
        (id INTEGER PRIMARY KEY, 
        name TEXT)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS data
        (id INTEGER PRIMARY KEY, 
        pollutant_id INTEGER, 
        station_id INTEGER, 
        date TEXT, 
        value REAL,
        FOREIGN KEY (pollutant_id)
        REFERENCES pollutants(id),
        FOREIGN KEY (station_id)
        REFERENCES stations(id)
        )""")
    cursor.commit()
    connection.close()


def update_stations(sqlitefilename, stations):
    connection = sqlite3.connect(sqlitefilename)
    cursor = connection.cursor()
    for row in cursor.execute("""SELECT * FROM stations WHERE name LIKE ?""", name):
        print(cursor.fetchall())


def read_data_file(filename):
    print(os.path.basename(filename))
    try:
        with open(filename, "r") as f:
            data = json.load(f)
            for pollutant in data:
                try:
                    for dates in pollutant['data']:
                        print(pollutant['keyword'],
                              dates['date'], dates['value'])
                except KeyError:
                    pass
    except Exception as e:
        print("File " + filename + " is not accessible. ", e)



sqlitefilename = "pollution-data.db"

if len(argv) > 1:
    for filename in argv[1:]:
        read_data_file(filename)
else:
    print("Usage: " + __file__ + " data_files")
