import re
import json
import datetime
import requests

url = "http://gov.meteo.kg/?map=5"
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)'
    ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}
response = requests.get(url, headers=headers)
response.encoding = 'utf-8'

curdate = datetime.datetime.today().strftime("%Y%m%d")
filename_prefix = "output/"

station_id = 0
try:
    with open(filename_prefix + "stations_" + curdate + ".txt", "w") \
            as stations_file:
        for lines in response.text.splitlines():
            linea = lines.lstrip()
            if re.match("(var content \= \[)", linea):
                with open(filename_prefix + "data_" + curdate + "_" +
                          str(station_id) + ".txt", "w") as f:
                    result = re.search("\[", linea)
                    (pos, length) = result.span()
                    linea = linea[pos:-1]
                    f.write(linea + '\n')
                    station_id += 1

            if re.match("wicon", lines):
                lineb = lines.replace(
                    "wicon(", "").replace(", content);", "").replace(
                    "<br>", "")
                stations_file.write(lineb + '\n')
except Exception as e:
    raise

print(station_id, "stations saved")
