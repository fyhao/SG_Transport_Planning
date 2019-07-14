# MRT dijsktra algorithm
from collections import defaultdict
import json
class Graph():
    def __init__(self):
        """
        self.edges is a dict of all possible next nodes
        e.g. {'X': ['A', 'B', 'C', 'E'], ...}
        self.weights has all the weights between two nodes,
        with the two nodes as a tuple as the key
        e.g. {('X', 'A'): 7, ('X', 'B'): 2, ...}
        """
        self.edges = defaultdict(list)
        self.weights = {}
    
    def add_edge(self, from_node, to_node, weight):
        # Note: assumes edges are bi-directional
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.weights[(from_node, to_node)] = weight
        self.weights[(to_node, from_node)] = weight


def dijsktra(graph, initial, end):
    # shortest paths is a dict of nodes
    # whose value is a tuple of (previous node, weight)
    shortest_paths = {initial: (None, 0)}
    current_node = initial
    visited = set()
    
    current_str = current_node.split(':')[1]
    end_str = end.split(':')[1]
    while current_str != end_str:
        visited.add(current_node)
        destinations = graph.edges[current_node]
        weight_to_current_node = shortest_paths[current_node][1]

        for next_node in destinations:
            weight = graph.weights[(current_node, next_node)] + weight_to_current_node
            if next_node not in shortest_paths:
                shortest_paths[next_node] = (current_node, weight)
            else:
                current_shortest_weight = shortest_paths[next_node][1]
                if current_shortest_weight > weight:
                    shortest_paths[next_node] = (current_node, weight)
        
        next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
        if not next_destinations:
            return "Route Not Possible"
        # next node is the destination with the lowest weight
        current_node = min(next_destinations, key=lambda k: next_destinations[k][1])
        current_str = current_node.split(':')[1]
        end_str = end.split(':')[1]
    
    # Work back through destinations in shortest path
    path = []
    while current_node is not None:
        path.append(current_node)
        next_node = shortest_paths[current_node][0]
        current_node = next_node
    # Reverse path
    path = path[::-1]
    return path
    
def debug(msg):
    enabled = True
    if enabled:
        print(msg)

routes = [
    
]
with open('routes.json', 'r') as f:
    busRoutes = json.load(f)

# first link route for shared BusStopCode
'''
debug("Total busRoutes: " + str(len(busRoutes)))
processed = 0
for r in busRoutes:
    processed = processed + 1
    #if processed > 1000:
    #    break;
    debug('Processed: ' + str(processed) + '/' + str(len(busRoutes)))
    for y in busRoutes:
        if r['BusStopCode'] == y['BusStopCode'] and r['ServiceNo'] != y['ServiceNo']:
            routes.append([r['ServiceNo'] + ":" + r['BusStopCode'],y['ServiceNo'] + ":" + y['BusStopCode']])
debug('Processed routes: ' + str(len(routes)))         
with open('bus.json', 'w') as f:
    json.dump(routes, f)
'''  
with open('bus.json', 'r') as f:
    routes = json.load(f)
    
lastServiceNo = ''
lastRoute = []
for r in busRoutes:
    if r['ServiceNo'] != lastServiceNo:
        lastRoute = []
        routes.append(lastRoute)
        lastServiceNo = r['ServiceNo']
    
    lastRoute.append(r['ServiceNo'] + ":" + r['BusStopCode'])

#print("Routes:")
#print(routes)    
breakDownRoutes = []
#breakDownRoutes.append(['NS13','NS12','NS11'])

def internal_plan_path(source,dest):
    debug("DEBUG source=" + source + ", dest=" + dest)
    graph = Graph()
    edges = []
   
    for route in routes:
        i = 0
        while i < len(route) - 1:
            cost = 1
            arr1 = route[i].split(':')
            arr2 = route[i+1].split(':')
            sn1 = arr1[0]
            sn2 = arr2[0]
            if sn1 != sn2:
                cost = 5 #change bus
            edges.append((route[i], route[i+1],cost))
            i = i+1

    for edge in edges:
        graph.add_edge(*edge)
    
    source = [r for r in busRoutes if r['BusStopCode'] == source][0]
    dest = [r for r in busRoutes if r['BusStopCode'] == dest][0]
    source = source['ServiceNo'] + ':' + source['BusStopCode']
    dest = dest['ServiceNo'] + ':' + dest['BusStopCode']
    a = dijsktra(graph, source, dest)
    return a


stops = []
with open('stops.json', 'r') as f:
    stops = json.load(f)   

def formatBusStop(field1, field2, source):
    stop1 = [s[field1] for s in stops if s[field2] == source]
    if len(stop1) > 0:
        return stop1[0]
    return None
    
    
def plan_path(source, dest):
    stop1 = formatBusStop("BusStopCode", "Description", source)
    stop2 = formatBusStop("BusStopCode", "Description", dest)
    if stop1 == None or stop2 == None:
        return None
    
    result = internal_plan_path(stop1, stop2)
    result = [{"ServiceNo" : r.split(':')[0], 'BusStopCode' : r.split(':')[1]} for r in result]
    return result
    
def plan_path_by_code(source, dest):
    stop1 = source
    stop2 = dest
    if stop1 == None or stop2 == None:
        return None
    
    result = internal_plan_path(stop1, stop2)
    result = [{"ServiceNo" : r.split(':')[0], 'BusStopCode' : r.split(':')[1]} for r in result]
    return result

def print_result(result):
    res = ["Service No: " + r["ServiceNo"] + " at Bus Stop " + formatBusStop("Description", "BusStopCode", r["BusStopCode"]) for r in result]
    for i in res:
        print(i)

def print_guide(result):
    lastServiceNo = ''
    lastBusStop = ''
    taken = False
    res = []
    noOfStops = 0
    lastNoOfStops = 0
    for r in result:
        if lastServiceNo != r["ServiceNo"]:
            if taken == False:
                place = formatBusStop("Description", "BusStopCode", r["BusStopCode"])
                res.append("Take bus " + r["ServiceNo"] + " at " + place)
                taken = True
            else:
                lastPlace = formatBusStop("Description", "BusStopCode", lastBusStop)
                res.append("Alight at " + lastPlace + " after " + str(noOfStops) + " stops")
                place = formatBusStop("Description", "BusStopCode", r["BusStopCode"])
                res.append("Take bus " + r["ServiceNo"] + " at " + place)
            
            noOfStops = 0
        else:
            noOfStops = noOfStops + 1
            lastNoOfStops = noOfStops
            
        lastServiceNo = r["ServiceNo"]
        lastBusStop = r["BusStopCode"]
    lastPlace = formatBusStop("Description", "BusStopCode", lastBusStop)
    res.append("Alight at " + lastPlace + " after " + str(lastNoOfStops) + " stops and reached destination")
    for i in res:
        print(i)
        
print("Result:")
#r = plan_path('Clementi Stn',"Opp S'pore Expo")
r = plan_path_by_code('70231',"49121")
print_result(r)
print("-----")
print_guide(r)