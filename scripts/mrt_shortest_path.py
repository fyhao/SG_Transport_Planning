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
    
    while current_node != end:
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
'''
# build EW1 to EW33
ewRoute = []
for i in range(33):
    ewRoute.append('EW' + str(i+1))
routes.append(ewRoute)
nsRoute = []
for i in range(26):
    nsRoute.append('NS' + str(i+1))
routes.append(nsRoute)
routes.append(['EW24','NS1'])
routes.append(['EW13','NS25'])
routes.append(['EW14','NS26'])

ccRoute = []
for i in range(29):
    ccRoute.append('CC' + str(i+1))
routes.append(ccRoute)
routes.append(['CC22','EW21'])
routes.append(['CC15','NS17'])
routes.append(['CC9','EW8'])
routes.append(['CC1','NS24'])

neRoute = []
for i in range(17):
    neRoute.append('NE' + str(i+1))
routes.append(neRoute)
routes.append(['NE1','CC29'])
routes.append(['NE3','EW16'])
routes.append(['NE6','CC1'])
routes.append(['NE6','NS24'])
routes.append(['NE12','CC13'])

dtRoute = []
for i in range(37):
    dtRoute.append('DT' + str(i+1))
routes.append(dtRoute)
routes.append(['DT9','CC19'])
routes.append(['DT11','NS21'])
routes.append(['DT12','NE7'])
routes.append(['DT14','EW12'])
routes.append(['DT15','CC4'])
routes.append(['DT19','NE4'])
routes.append(['DT26','CC10'])
routes.append(['DT32','EW2'])

with open('mrt.json', 'w') as f:
    json.dump(routes, f)
'''   
with open('mrt.json', 'r') as f:
    routes = json.load(f)
breakDownRoutes = []
breakDownRoutes.append(['NS13','NS12','NS11'])

def plan_path(source,dest):
    debug("DEBUG source=" + source + ", dest=" + dest)
    graph = Graph()
    edges = []
    
    # find a cross if route[i] (which is the route when same as source) both exist in both routes, and 
    # source not in the array same as route[i]
    # then the cost of other route[i] to route[i+1] must be larger than 1
    # first find the route that source is inside
    route_source = []
    for route in routes:
        if source in route:
            route_source.append(route)
    debug('route source:')
    debug(route_source)
    
    for route in routes:
        i = 0
        while i < len(route) - 1:
            cost = 1
            if source not in route:
                for rs in route_source:
                    if route[i] in rs:
                        cost = 5
            
            # if route A and B is different prefix (MRT)
            if route[i][:2] != route[i+1][:2]:
                cost = 5
            
            # Check breakdown route and ignore
            isBreakDown = False
            for r in breakDownRoutes:
                if route[i] in r and route[i+1] in r:
                    isBreakDown = True
            
            if not isBreakDown:
                debug("DEBUG route " + route[i] + ", " + route[i+1] + ", cost=" + str(cost))
                edges.append((route[i], route[i+1],cost))
            
            i = i+1

    for edge in edges:
        graph.add_edge(*edge)

    a = dijsktra(graph, source, dest)
    return a

print(plan_path('CC10','NS7'))

#reference:
# http://benalexkeen.com/implementing-djikstras-shortest-path-algorithm-with-python/
# http://www.lihaoyi.com/post/PlanningBusTripswithPythonSingaporesSmartNationAPIs.html#dijkstras-algorithm
# 2