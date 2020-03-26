"""This script fetches air pollution data from gov.meteo.kg website and saves it"""

import re
import datetime
import requests

URL = "http://gov.meteo.kg/?map=5"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)'
                  ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}
RESPONSE = requests.get(URL, headers=HEADERS)
RESPONSE.encoding = 'utf-8'

CURDATE = datetime.datetime.today().strftime("%Y%m%d")
FILENAME_PREFIX = "output/"

STATION_ID = 0
try:
    with open(FILENAME_PREFIX + "stations_" + CURDATE + ".txt", "w") \
            as stations_file:
        for lines in RESPONSE.text.splitlines():
            linea = lines.lstrip()
            if re.match(r"(var content \= \[)", linea):
                with open(FILENAME_PREFIX + "data_" + CURDATE + "_" +
                          str(STATION_ID) + ".txt", "w") as f:
                    result = re.search(r"\[", linea)
                    (pos, length) = result.span()
                    linea = linea[pos:-1]
                    f.write(linea + '\n')
                    STATION_ID += 1

            if re.match("wicon", lines):
                lineb = lines.replace(
                    "wicon(", "").replace(", content);", "").replace(
                        "<br>", "")
                stations_file.write(lineb + '\n')
        print(STATION_ID, "stations saved")
except FileNotFoundError as error:
    print("Error saving files:", error)
