import json

class LocationManager:
    def __init__(self, json_file="data/campus_map.json"):
        # Dictionary to store locations with their coordinates
        self.locations = {}
        self.json_file = json_file
        self.load_locations()

    def load_locations(self):
        """Load locations from the JSON file."""
        try:
            with open(self.json_file, "r") as file:
                data = json.load(file)
                for location in data.get("locations", []):
                    name = location["name"]
                    coordinates = location.get("coordinates", "0,0")
                    self.locations[name] = coordinates
            print("Locations loaded successfully.")
        except FileNotFoundError:
            print(f"File {self.json_file} not found. Starting with an empty location list.")
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {self.json_file}. Starting with an empty location list.")

    def save_locations(self):
        """Save locations to the JSON file."""
        try:
            data = {"locations": [{"name": name, "coordinates": coords} for name, coords in self.locations.items()]}
            with open(self.json_file, "w") as file:
                json.dump(data, file, indent=4)
            print("Locations saved successfully.")
        except Exception as e:
            print(f"Error saving locations: {e}")

    def add_location(self, name, coordinates):
        """Add a new location."""
        if name in self.locations:
            print(f"Location '{name}' already exists.")
        else:
            self.locations[name] = coordinates
            print(f"Location '{name}' added with coordinates {coordinates}.")
            self.save_locations()

    def edit_location(self, name, new_coordinates):
        """Edit an existing location."""
        if name in self.locations:
            self.locations[name] = new_coordinates
            print(f"Location '{name}' updated to new coordinates {new_coordinates}.")
            self.save_locations()
        else:
            print(f"Location '{name}' does not exist.")

    def delete_location(self, name):
        """Delete a location."""
        if name in self.locations:
            del self.locations[name]
            print(f"Location '{name}' deleted.")
            self.save_locations()
        else:
            print(f"Location '{name}' does not exist.")

    def search_location(self, name):
        """Search for a location by name."""
        return self.locations.get(name, None)

    def list_locations(self):
        """List all locations on the campus map."""
        if not self.locations:
            print("No locations available on the campus map.")
        else:
            print("Current locations on the campus map:")
            for name, coordinates in self.locations.items():
                print(f"- {name}: {coordinates}")