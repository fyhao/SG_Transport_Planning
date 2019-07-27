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
with open('mrt.json', 'r') as f:
    mrtRoutes = json.load(f)
    
with open('bus.json', 'r') as f:
    busRoutes = json.load(f)
    
with open('bus_mrt_routes.json', 'r') as f:
    busMrtRoutes = json.load(f)
    
graph = Graph()
edges = []

for route in busRoutes:
    i = 0
    while i < len(route) - 1:
        cost = 1
        arr1 = route[i].split(':')
        arr2 = route[i+1].split(':')
        sn1 = arr1[0]
        sn2 = arr2[0]
        if sn1 != sn2:
            cost = 1 #change bus
        edges.append((route[i], route[i+1],cost))
        i = i+1
        


for route in mrtRoutes:
    i = 0
    while i < len(route) - 1:
        cost = 2000
        
        # if route A and B is different prefix (MRT)
        if route[i][:2] != route[i+1][:2]:
            cost = cost * 15
        
        # Check breakdown route and ignore
        isBreakDown = False
        
        if not isBreakDown:
            #debug("DEBUG route " + route[i] + ", " + route[i+1] + ", cost=" + str(cost))
            edges.append((route[i], route[i+1],cost))
        
        i = i+1
        
for route in busMrtRoutes:
    cost = 1
    if ':' in route[0]:
        type0 = 'bus'
    else:
        type0 = 'mrt'
    if ':' in route[1]:
        type1 = 'bus'
    else:
        type1 = 'mrt'

    if type0 == 'bus' and type1 == 'mrt':
        cost = 10
    else:
        cost = 1
    edges.append((route[0], route[1],cost))
    
for edge in edges:
    graph.add_edge(*edge)
    
# Test
source = '170:40041'
dest = 'NS1'
a = dijsktra(graph, source, dest)
print(a)