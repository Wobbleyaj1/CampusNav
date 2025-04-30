import json
from data_structures.dictionary import twoWayDict
class LocationManager:
    def __init__(self, json_file="data/campus_map.json", features_file="data/location_features.json"):
        # List to store locations with their full structure
        self.locations = []
        self.json_file = json_file
        self.location_features = {}
        self.features_file = features_file
        self.load_locations()

    def load_locations(self):
        """Load locations from the JSON file."""
        try:
            with open(self.json_file, "r") as file:
                data = json.load(file)
                self.locations = data.get("locations", [])
            print("Locations loaded successfully.")
        except FileNotFoundError:
            print(f"File {self.json_file} not found. Starting with an empty location list.")
            self.locations = []
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {self.json_file}. Starting with an empty location list.")
            self.locations = []

        try:
            with open(self.features_file, "r") as file:
                self.location_features = json.load(file)
                print(self.location_features)
            print("Locations loaded successfully.")
        except FileNotFoundError:
            print(f"File {self.features_file} not found. Starting with an empty feature dictionary.")
            self.location_features = {}
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {self.features_file}. Starting with an empty feature dictionary.")
            self.location_features = {}

    def get_visible_Locations(self):
        return [loc for loc in self.locations if loc['pointOfInterest']]

    def search_location(self, name):
        """Search for a location by name."""
        for location in self.locations:
            if location["name"] == name:
                return location
        return None

    def list_location_names(self):
        """List all locations on the campus map."""
        if not self.locations:
            print("No locations available on the campus map.")
        else:
            print("Current locations on the campus map:")
            for location in self.locations:
                print(f"- {location['name']}: ({location['x']}, {location['y']})")

    def get_location_names(self) -> list[str]:
        l = []
        for location in self.locations:
            if location['pointOfInterest']:
                l.append(location['name'])
        return l

    def get_location_ids(self) -> list[int]:
        ids = []
        for location in self.locations:
            ids.append(location['id'])
        return ids
    
    def get_location_id(self, name: str) -> int:
        for location in self.locations:
            if location['name'] == name:
                return location['id']
        raise KeyError(f'The name "{name}" does not exit.')
    
    def get_location_name(self, id: int) -> str:
        for location in self.locations:
            if location['id'] == id:
                return location['name']
        raise KeyError(f'The id "{id}" does not exist.')
    
    def get_location_name_from_cords(self, x: int, y: int) -> str:
        for location in self.locations:
            if location['x'] == x and location['y'] == y:
                return location['name']
        raise KeyError(f'A point at "{x},{y}" does not exist.')
    
    def get_location_coordinates(self, id: int) -> tuple[int, int]:
        """Get the coordinates (x, y) of a location by its ID."""
        for location in self.locations:
            if location["id"] == id:
                return location["x"], location["y"]
        raise KeyError(f'The id "{id}" does not exist.')
    
    def is_point_of_interest(self, name: str) -> bool:
        for location in self.locations:
            if location['name'] == name:
                return location['pointOfInterest']
        raise KeyError(f'The name "{name}" does not exit.')