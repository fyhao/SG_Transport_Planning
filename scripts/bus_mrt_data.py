import json
with open('stops.json', 'r') as f:
    stops = json.load(f)

with open('mrt_stations.json', 'r') as f:
    mrt_stations = json.load(f)
    
with open('routes.json', 'r') as f:
    busRoutes = json.load(f)
    
mrtStops = [stop for stop in stops if 'Stn' in stop['Description']]

print(mrtStops)
mrtStops2 = [{"BusStopCode":stop['BusStopCode'], 'Stn':stop['Description'].replace('Stn','').replace('Opp','').strip()} for stop in mrtStops]
print(mrtStops2)
print(mrt_stations)
mrtStations = [{"StnCode":m["Station"], "Stn":m["Station Name"]} for m in mrt_stations]
print(mrtStations)

bus_mrt_mapping = [{"BusStopCode":x["BusStopCode"],"StnCode":y["StnCode"],"Stn":y["Stn"]} for x in mrtStops2 for y in mrtStations if x["Stn"] == y["Stn"]]
print(bus_mrt_mapping)

print("Testing")
print("mrtStops2")
print([x for x in mrtStops2 if x['Stn'] == 'Simei'])
print("mrtStations")
print([x for x in mrtStations if x['Stn'] == 'Simei'])
print("bus_mrt_mapping")
print([x for x in bus_mrt_mapping if x['Stn'] == 'Simei'])
print("busRoutes")
print([x for x in busRoutes if x["BusStopCode"] == '96149'])

bus_mrt_mapping2 = [{'ServiceBus':y['ServiceNo'] + ':' + y['BusStopCode'],'StnCode':x['StnCode'],'Stn':x['Stn']} for x in bus_mrt_mapping for y in busRoutes if x['BusStopCode'] == y['BusStopCode']]
print(bus_mrt_mapping2)
with open('bus_mrt.json', 'w') as f:
    json.dump(bus_mrt_mapping2, f)
    
busMrtRoutes = []
for data in bus_mrt_mapping2:
    busMrtRoutes.append([data['ServiceBus'],data['StnCode']])
    
print(busMrtRoutes)
with open('bus_mrt_routes.json', 'w') as f:
    json.dump(busMrtRoutes, f)