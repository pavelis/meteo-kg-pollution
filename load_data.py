import re
import json

filename = "output/20200207_data_0.txt"

with open(filename, "r") as f:
	data = json.load(f)
	f.close()
	for pollutant in data:
		try:
			for dates in pollutant['data']:
				print(pollutant['keyword'], dates['date'], dates['value'])
		except Exception as e:
			pass
