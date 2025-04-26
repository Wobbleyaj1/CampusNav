import json
from data_structures.dictionary import twoWayDict
class LocationManager:
    def __init__(self, json_file="data/campus_map.json"):
        # List to store locations with their full structure
        self.locations = []
        self.json_file = json_file
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

    def save_locations(self):
        """Save locations to the JSON file."""
        try:
            data = {"locations": self.locations}
            with open(self.json_file, "w") as file:
                json.dump(data, file, indent=4)
            print("Locations saved successfully.")
        except Exception as e:
            print(f"Error saving locations: {e}")

    def add_location(self, name, coordinates, point_of_interest):
        """Add a new location."""
        # Check if the location already exists
        if any(location["name"] == name for location in self.locations):
            print(f"Location '{name}' already exists.")
            return

        # Parse coordinates
        try:
            x, y = map(int, coordinates.split(","))
        except ValueError:
            print("Invalid coordinates format. Use 'x,y'.")
            return

        # Generate a new unique ID
        new_id = max((location["id"] for location in self.locations), default=0) + 1

        # Add the new location
        new_location = {
            "id": new_id,
            "name": name,
            "x": x,
            "y": y,
            "pointOfInterest": point_of_interest
        }
        self.locations.append(new_location)
        print(f"Location '{name}' added with coordinates {coordinates} and pointOfInterest={point_of_interest}.")
        self.save_locations()

    def edit_location(self, name, new_coordinates):
        """Edit an existing location."""
        for location in self.locations:
            if location["name"] == name:
                try:
                    x, y = map(int, new_coordinates.split(","))
                except ValueError:
                    print("Invalid coordinates format. Use 'x,y'.")
                    return
                location["x"] = x
                location["y"] = y
                print(f"Location '{name}' updated to new coordinates {new_coordinates}.")
                self.save_locations()
                return
        print(f"Location '{name}' does not exist.")

    def delete_location(self, name):
        """Delete a location."""
        for location in self.locations:
            if location["name"] == name:
                self.locations.remove(location)
                print(f"Location '{name}' deleted.")
                self.save_locations()
                return
        print(f"Location '{name}' does not exist.")

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