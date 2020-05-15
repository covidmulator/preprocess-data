import datetime, json
import numpy as np
import cv2
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
sns.set()

fields = []
date = '200509'

with open(f'turnstile_{date}.txt', 'r') as file:
  data = file.readlines()

with open('normed_coordinates.json', 'r') as file:
  locations = json.load(file)

def parse_data (line):
  res = {}
  for (index, field) in enumerate(fields):
    res[field] = line[index]

  res['ENTRIES'] = int(res['ENTRIES'])
  res['EXITS'] = int(res['EXITS'])
  
  return res

print('Analyzing...')

data = list(map(lambda line: line.strip().split(','), data))

fields = data[0]
data = data[1:]

data = list(map(parse_data, data))

turnstile = {}

data_size = len(data)

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

def z_score_normalize(lst):
  normalized = []
  for value in lst:
    normalized_num = (value - np.mean(lst)) / np.std(lst)
    normalized.append(normalized_num)
  return normalized

print('Tensorizing...')

tensor_height = 35
tensor_width = 35
tensor_size = (tensor_height, tensor_width)

not_exist = [
  "CITY / BUS",
  "LACKAWANNA",
  "NEWARK BM BW",
  "NEWARK C",
  "NEWARK HM HE",
  "PAVONIA/NEWPORT",
  "NEWARK HW BMEBE"
]

stations = list(locations.keys())

for time in list(turnstile.keys()):
  tensor = np.zeros(tensor_size)
  for index, station in enumerate(stations):
    if station in not_exist:
      continue

    location = locations[station]
    try:
      value = turnstile[time][station]    
    except:
      continue

    x = location[0] * tensor_width
    y = location[1] * tensor_height

    tensor[int(x)][int(y)] = 10000

  break
