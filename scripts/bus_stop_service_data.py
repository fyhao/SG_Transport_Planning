# MRT dijsktra algorithm
from collections import defaultdict
import json
with open('routes.json', 'r') as f:
    routes = json.load(f)
    
with open('stops.json', 'r') as f:
    stops = json.load(f)
    
with open('services.json', 'r') as f:
    services = json.load(f)
    
stopServiceData = {}

for route in routes:
    key = route['BusStopCode'];
    if key not in stopServiceData:
        stopServiceData[key] = []
    item = {'ServiceNo':route["ServiceNo"]}
    serviceData = [x for x in services if x['ServiceNo'] == route['ServiceNo']][0]
    for k in serviceData:
        item[k] = serviceData[k]
    stopServiceData[key].append(item)

with open('stopServiceData.json', 'w') as f:
    json.dump(routes, f)
    
print(stopServiceData)