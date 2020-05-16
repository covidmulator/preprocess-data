import datetime, json
import matplotlib.pyplot as plt
import osmnx as ox
import requests
from utils\
  import min_max_normalize, not_exist, url_generator, fields

with open('turnstile_dates.json', 'r') as file:
  dates = json.load(file)

with open('coordinates.json', 'r') as file:
  locations = json.load(file)

def parse_data (line):
  res = {}
  for index, field in enumerate(fields):
    res[field] = line[index]

  res['ENTRIES'] = int(res['ENTRIES'])
  res['EXITS'] = int(res['EXITS'])
  
  return res

for date in dates:
  print(date)
  print('Analyzing...')

  data = requests.get(url_generator(date)).text
  data = data.split('\n')
  data = list(map(lambda x: x.strip(), data))
  data = list(map(lambda x: x.split(','), data))
  data = data[:-1]

  if int(date) > 141011:
    data = data[1:]

  data = list(map(parse_data, data))
  turnstile = {}

  for index, stamp in enumerate(data):
    stamp['DATE'] = stamp['DATE'].split('/')
    stamp['DATE'] = list(map(lambda x: int(x), stamp['DATE']))

    stamp['TIME'] = stamp['TIME'].split(':')
    stamp['TIME'] = list(map(lambda x: int(x), stamp['TIME']))

    timestamp = int(datetime.datetime(
      stamp['DATE'][2], stamp['DATE'][0], stamp['DATE'][1],
      stamp['TIME'][0], 0, 0).timestamp())

    if timestamp not in turnstile:
      turnstile[timestamp] = {}
    if stamp['STATION'] not in turnstile[timestamp]:
      turnstile[timestamp][stamp['STATION']] = 0
    
    turnstile[timestamp][stamp['STATION']] += stamp['ENTRIES'] - stamp['EXITS']

  print('Normalizing...')

  for time in list(turnstile.keys()):
    values = []
    for _, key in enumerate(list(turnstile[time].keys())):
      values.append(turnstile[time][key])
    values = min_max_normalize(values)
    for index, key in enumerate(list(turnstile[time].keys())):
      turnstile[time][key] = values[index]

  print('Tensorizing...')

  original_G = ox.graph_from_place('New York City, New York, USA', network_type='drive')

  for time in list(turnstile.keys()):
    G = original_G
    fig, ax = ox.plot_graph(G, show=False, close=False, node_size=0, edge_linewidth=0)

    stations = list(turnstile[time].keys())
    for index, station in enumerate(stations):
      if station in not_exist:
        continue

      coordinate = locations[station]
      value = turnstile[time][station]

      color = '#%02x%02x%02x' % (int(value * 255), 0, 0)
      ax.scatter(coordinate[1], coordinate[0], c=color, linewidths=4*value, alpha=0.5)
    plt.savefig(f'generated_tensors/{date}_{time}.png')
