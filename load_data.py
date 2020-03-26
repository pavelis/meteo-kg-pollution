"""This script loads raw air pollution data and structurize it"""

import json
import os.path
from sys import argv

def read_data_file(filename):
    """Reads raw data file and prints out data"""
    print(os.path.basename(filename))
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            for pollutant in data:
                try:
                    for dates in pollutant['data']:
                        print(pollutant['keyword'],
                              dates['date'], dates['value'])
                except KeyError:
                    pass
    except FileNotFoundError as error:
        print("File " + filename + " is not accessible. ", error)


if len(argv) > 1:
    for name in argv[1:]:
        read_data_file(name)
else:
    print("Usage: " + __file__ + " data_files")
