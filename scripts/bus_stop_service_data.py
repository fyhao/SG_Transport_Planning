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
    oldItem = [x for x in stopServiceData[key] if x['ServiceNo'] == route['ServiceNo']]
    if(len(oldItem) == 0): 
        stopServiceData[key].append(item)

with open('stopServiceData.json', 'w') as f:
    json.dump(stopServiceData, f)
    
##print(stopServiceData)
print(stopServiceData['70231'])