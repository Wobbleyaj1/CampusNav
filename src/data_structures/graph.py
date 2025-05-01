# An Undirected Graph data structure
import heapq
import json

class Graph:
    def __init__(self):
        """Initialize the graph."""
        self.paths = dict[int, dict[int, int]]()
        self.node_count = 0
        self.edge_count = 0

    def add_node(self, id: int):
        """Add a new node to the graph."""
        if id in self.paths:
            raise ValueError(f'{id} is already a node.')
        self.paths[id] = dict()
        self.node_count += 1

    def add_edge(self, id_1: int, id_2: int, weight:int):
        """Add a bidirectional edge between two nodes."""
        if id_1 not in self.paths:
            raise ValueError(f'ID 1 ({id_1}) is not a valid node.')
        if id_2 not in self.paths:
            raise ValueError(f'ID 2 ({id_2}) is not a valid node.')

        self.paths[id_1][id_2] = weight
        self.paths[id_2][id_1] = weight

        self.edge_count += 1

    def remove_node(self, id: int):
        """Remove a node and all connected edges."""
        connectedNodes = list(self.paths[id])
        self.paths.pop(id)
        for node in connectedNodes:
            self.paths[node].pop(id)

        self.node_count -= 1

    def remove_edge(self, id_1: int, id_2: int):
        self.paths[id_1].pop(id_2)
        self.paths[id_2].pop(id_1)

        self.edge_count -= 1

    def get_edge_weight(self, id_1:int, id_2:int) -> int:
        try:
            return self.paths[id_1][id_2]
        except:
            raise KeyError(f'Edge between {id_1} & {id_2} does not exist.')

    def find_shortest_path(self, start_id: int, end_id: int) -> tuple[list[int], int]:
        """Find the shortest path using Dijkstra like BFS"""
        heap = [(0, start_id, [start_id])]
        visited = set()

        while heap:
            curr_dis, current, path = heapq.heappop(heap)
            if current == end_id:
                return path, curr_dis
            
            if current in visited:
                continue
            visited.add(current)

            for neighbor in self.paths[current]:
                if neighbor not in visited:
                    edge_weight = self.get_edge_weight(current, neighbor)
                    heapq.heappush(heap, (curr_dis + edge_weight, neighbor, path + [neighbor]))

        return [], 10**6

    def __str__(self):
        s = ''
        for node in self.paths:
            s += f'{node}: {self.paths[node]}\n'
        return s
    
    def load_from_json(self, json_file: str):
        """Load nodes and edges from a JSON file."""
        try:
            with open(json_file, "r") as file:
                data = json.load(file)
                connections = data.get("connections", [])
                for connection in connections:
                    self.add_edge(connection['from'], connection['to'], connection['distance'])
            print('Graph built successfully from JSON.')
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {json_file}. Graph will have no connections.")
        except FileNotFoundError:
            print(f"JSON file {json_file} not found.")