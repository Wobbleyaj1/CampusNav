from location_manager import LocationManager
from route_history import RouteHistory
from data_structures.graph import Graph
from utils import plot_locations

def main():
    # Initialize components
    location_manager = LocationManager()
    route_history = RouteHistory()
    graph = graph()

    print("Welcome to Campus Navigation System!")

    while True:
        # Display menu options
        print("\nMenu:")
        print("1. Add a new location")
        print("2. Edit an existing location")
        print("3. Delete a location")
        print("4. Search for a location")
        print("5. Find shortest route between two locations")
        print("6. View route history")
        print("7. Display all locations on the campus map")
        print("8. Exit")

        # Get user input
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 8.")
            continue

        # Handle user choice
        if choice == 1:
            # Add a new location
            location_name = input("Enter location name: ")
            coordinates = input("Enter coordinates (e.g., x,y): ")
            location_manager.add_location(location_name, coordinates)
            print("Location added successfully!")

        elif choice == 2:
            # Edit an existing location
            location_name = input("Enter location name to edit: ")
            new_coordinates = input("Enter new coordinates (e.g., x,y): ")
            location_manager.edit_location(location_name, new_coordinates)
            print("Location updated successfully!")

        elif choice == 3:
            # Delete a location
            location_name = input("Enter location name to delete: ")
            location_manager.delete_location(location_name)
            print("Location deleted successfully!")

        elif choice == 4:
            # Search for a location
            location_name = input("Enter location name to search: ")
            result = location_manager.search_location(location_name)
            if result:
                print(f"Location found: {result}")
            else:
                print("Location not found.")

        elif choice == 5:
            # Find shortest route between two locations
            start_location = input("Enter start location: ")
            end_location = input("Enter end location: ")
            route = graph.find_shortest_path(start_location, end_location)
            if route:
                print(f"Shortest route: {route}")
                route_history.add_route(route)
            else:
                print("No route found between the locations.")

        elif choice == 6:
            # View route history
            history = route_history.get_history()
            print("Route History:")
            for route in history:
                print(route)

        elif choice == 7:
            # Display all locations on the campus map
            plot_locations(location_manager.locations, background_image_path="./assets/mercer_map.png")

        elif choice == 8:
            # Exit the application
            print("Thank you for using Campus Navigation System!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()