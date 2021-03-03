"""This script loads raw air pollution data and saves it into CSV file"""

import re
import json
import os.path
from sys import argv
import pandas as pd


def read_data_file(filename):
    """Reads raw data file and prints out data"""
    dataset = []
    station_id = re.search(r"\_(\d{1,2})\.txt", filename).group(1)
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            for pollutant in data:
                try:
                    kwd = str(pollutant['name']['en'] if pollutant['id'] == 13 else pollutant['keyword'])
                    for dates in pollutant['data']:
                        date = pd.Timestamp(dates['date'])
                        value = float(dates['value']) / 1000 if date >= pd.Timestamp(2021, 2, 26) else float(dates['value'])
                        dataset.append([pd.Timestamp(dates['date']), int(station_id), kwd, value])
                except KeyError:
                    pass
            dataframe = pd.DataFrame(dataset, columns=['date', 'station', 'pollutant', 'value'])
            return dataframe
    except FileNotFoundError as error:
        print("File " + filename + " is not accessible. ", error)


outfile_prefix = "kg_pollution"
dflist = pd.DataFrame()

if len(argv) > 1:
    for name in argv[1:]:
        dflist = pd.concat([dflist, read_data_file(name)], ignore_index=True)
else:
    print("Usage: " + __file__ + " data_files")

dflist = dflist.convert_dtypes()
dflist = dflist.drop_duplicates(subset=['date', 'station', 'pollutant'], keep='last', ignore_index=True)
dflist = dflist.sort_values(by=['date', 'station', 'pollutant'], ignore_index=True)
print(dflist)
ycounts = dflist.date.dt.year.drop_duplicates()
for y in ycounts:
    ylist = dflist[dflist['date'].dt.year == y]
    outfile = f"{outfile_prefix}_{str(y)}.csv"
    ylist.to_csv(outfile, index=False)
    print(f"{outfile} saved")
