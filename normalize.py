import numpy as np
import json
import math
from math import sin, cos, sqrt, atan2, radians

with open('coordinates.json', 'r') as raw_file:
    data = json.load(raw_file)

x = {}
y = {}
for _, station in enumerate(data):
    x[station] = data[station][0]
    y[station] = data[station][1]

def get_dist(a, b):
    R = 6373.0

    lat1 = radians(a[0])
    lon1 = radians(a[1])
    lat2 = radians(b[0])
    lon2 = radians(b[1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance

x_sorted = sorted(x.items(), key=lambda x: x[1])
y_sorted = sorted(y.items(), key=lambda x: x[1])

x_keys = list(map(lambda x: x[0], x_sorted))
y_keys = list(map(lambda x: x[0], y_sorted))

x_values = list(map(lambda x: x[1], x_sorted))
y_values = list(map(lambda x: x[1], y_sorted))

x_values = np.array(x_values)
y_values = np.array(y_values)
x_values = (x_values - np.min(x_values)) / (np.max(x_values) - np.min(x_values))
y_values = (y_values - np.min(y_values)) / (np.max(y_values) - np.min(y_values))

x_min = x_values[0]
y_min = y_values[0]

dist_x = []
dist_y = []

for index, x in enumerate(x_values):
    dist = get_dist([x, 0], [x_min, 0])
    dist_x.append((x_keys[index], x))

for index, y in enumerate(y_values):
    dist = get_dist([y, 0], [y_min, 0])
    dist_y.append((y_keys[index], y))

result = {}

for value in dist_x:
    result[value[0]] = [value[1], 0]
for value in dist_y:
    result[value[0]][1] = value[1]

result = json.dumps(result)
file = open('normed_coordinates.json', 'w')
file.write(result)
file.close()
