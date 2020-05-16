import json, csv
import datetime

res = []
date_format = '%m/%d/%Y %H:%M:%S'

with open('2016.csv', 'r') as file:
    data = csv.reader(file, delimiter=',', quotechar='|')
    
    header = True

    for row in data:
        if header:
            header = False
            continue

        date = row[6].split('T')[0]
        date = row[6] + ' ' + row[7]
        res.append({
            'exits': int(row[10]),
            'entries': int(row[9]),
            'station': row[3],
            'time': int(datetime.datetime.strptime(date, date_format).timestamp())
        })

res = json.dumps(res)
file = open('2016.json', 'w')
file.write(res)
file.close()
