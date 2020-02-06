import requests
import re
import datetime

#url = "http://pavel-i.com"
url = "http://gov.meteo.kg/?map=5"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
response = requests.get(url, headers = headers)
response.encoding = 'utf-8'

curdate = datetime.datetime.today().strftime("%Y%m%d")
filename = "../meteo-kg-pollution-data/" + curdate + ".txt"
print(filename)


with open(filename, "w") as f:

	for lines in response.text.splitlines():
		linea = lines.lstrip()
		if re.match("(var content \= \[)", linea):
			result = re.search("\[", linea)
			(pos, length) = result.span()
			linea = linea[pos:]
			print(linea)
			f.write(linea + '\n')
		if re.match("wicon", lines):
			#lineb = lines.replace("wicon(", "[").replace("content)", "content]")
			print(lines)
			f.write(lines + '\n')

	f.close()
