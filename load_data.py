import sqlite3
import json
from sys import argv

sqlitefilename = "pollution-data.db"

if len(argv) > 1:
	filename = argv[1]
else:
	print("Usage:", __file__, "data_file_name")
	exit()


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

try:
	with open(filename, "r") as f:
		data = json.load(f)
		for pollutant in data:
			try:
				for dates in pollutant['data']:
					print(pollutant['keyword'], dates['date'], dates['value'])
			except Exception as e:
				pass
except Exception as e:
	print("File", filename, "not accessible")
