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
                        dataset.append([dates['date'], station_id, kwd, dates['value']])
                except KeyError:
                    pass
            dataframe = pd.DataFrame(dataset, columns=['date', 'station', 'pollutant', 'value'])
            return dataframe
    except FileNotFoundError as error:
        print("File " + filename + " is not accessible. ", error)


OUTFILE = "outfile.csv"
dflist = pd.DataFrame()

if len(argv) > 1:
    for name in argv[1:]:
        dflist = pd.concat([dflist, read_data_file(name)], ignore_index=True)
else:
    print("Usage: " + __file__ + " data_files")

dflist = dflist.drop_duplicates(subset=['date', 'station', 'pollutant'], keep='last', ignore_index=True)
dflist = dflist.sort_values(by=['date', 'station', 'pollutant'], ignore_index=True)
print(dflist)
dflist.to_csv(OUTFILE, index=False)
