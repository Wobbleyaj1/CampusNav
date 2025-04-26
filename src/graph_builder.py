import json
from data_structures.graph import Graph

class graphBuilder():
    def __init__(self, graph: Graph, location_ids: int, json_file: str = "data/campus_map.json" ):
        for id in location_ids:
            graph.add_node(id)
        try:
            with open(json_file, "r") as file:
                    data = json.load(file)
                    connections = data.get("connections", [])
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {json_file}. Graph will have not connections.")
            return
        for connection in connections:
            graph.add_edge(connection['from'], connection['to'], connection['distance'])

        print('Graph built successfully')