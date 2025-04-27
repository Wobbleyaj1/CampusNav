# Standard Library Imports
import os

# Third-Party Imports
import tkinter as tk
from tkinter import simpledialog, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Local Imports
from location_manager import LocationManager
from route_history import RouteHistory
from data_structures.graph import Graph
from graph_builder import graphBuilder
from utils import extract_coordinates_and_labels, add_background_image, get_location_details, refresh_map, select_nearest_location

def display_map_with_menu(location_manager, route_history, graph):
    """Display the map and menu options in a single GUI window."""
    # Create the main tkinter window
    root = tk.Tk()
    root.title("Campus Navigation System")
    root.geometry("1000x800")

    def exit_application():
        """Exit the application cleanly."""
        print("Thank you for using Campus Navigation System!")
        root.destroy()
        os._exit(0)

    root.protocol("WM_DELETE_WINDOW", exit_application)

    # Create a frame for the map
    map_frame = tk.Frame(root)
    map_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Create a frame for the menu
    menu_frame = tk.Frame(root)
    menu_frame.pack(side=tk.BOTTOM, fill=tk.X)

    # Plot the map using matplotlib
    fig, ax = plt.subplots(figsize=(8, 6))
    x_coords, y_coords, labels = extract_coordinates_and_labels(location_manager.locations)
    add_background_image(ax, "./assets/mercer_map.png")
    ax.scatter(x_coords, y_coords, color="blue", label="Locations")
    for i, label in enumerate(labels):
        ax.annotate(label, (x_coords[i], y_coords[i]), textcoords="offset points", xytext=(5, 5), ha="center")
    ax.set_xlabel("X Coordinate")
    ax.set_ylabel("Y Coordinate")
    ax.set_title("Campus Map")
    ax.grid(True)
    ax.set_aspect(aspect = 1006 / 978)
    ax.legend()

    # Embed the matplotlib figure into the tkinter window
    canvas = FigureCanvasTkAgg(fig, master=map_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)

    # Define menu actions
    def add_location():
        """Allow the user to select a location on the current map and input details."""
        print("Click on the map to select a location.")

        # Variable to store the selected coordinates
        selected_coordinates = []

        # Event handler for mouse clicks
        def on_click(event):
            if event.xdata and event.ydata:
                # Ensure only one click is processed
                if selected_coordinates:
                    return

                selected_coordinates.append((int(event.xdata), int(event.ydata)))
                print(f"Selected coordinates: {selected_coordinates[0]}")

                # Disconnect the event handler after the first click
                fig.canvas.mpl_disconnect(cid)

                # Open a custom dialog to get location details
                location_name, point_of_interest = get_location_details(root)
                if not location_name:
                    print("No location name provided. Operation canceled.")
                    return

                # Add the new location to the location manager
                coordinates = f"{selected_coordinates[0][0]},{selected_coordinates[0][1]}"
                location_manager.add_location(location_name, coordinates, point_of_interest)
                print(f"Location '{location_name}' added at coordinates {coordinates} with pointOfInterest={point_of_interest}!")

                refresh_map(ax, canvas, selected_coordinates[0][0], selected_coordinates[0][1], location_name)

        # Connect the event handler to the matplotlib figure
        cid = fig.canvas.mpl_connect('button_press_event', on_click)

    def edit_location():
        """Allow the user to select a location on the map to edit."""
        print("Click on the map to select a location to edit.")

        def on_click(event):
            nearest_location = select_nearest_location(event, location_manager.locations)
            if nearest_location:
                print(f"Selected location: {nearest_location['name']}")
                fig.canvas.mpl_disconnect(cid)

                # Prompt for new coordinates
                new_coordinates = simpledialog.askstring("Input", "Enter new coordinates (x,y):", parent=root)
                location_manager.edit_location(nearest_location["name"], new_coordinates)
                print("Location updated successfully!")
                root.destroy()
                display_map_with_menu(location_manager, route_history, graph)

        # Connect the event handler to the matplotlib figure
        cid = fig.canvas.mpl_connect('button_press_event', on_click)

    def delete_location():
        """Allow the user to select a location on the map to delete."""
        print("Click on the map to select a location to delete.")

        def on_click(event):
            nearest_location = select_nearest_location(event, location_manager.locations)
            if nearest_location:
                print(f"Selected location: {nearest_location['name']}")
                fig.canvas.mpl_disconnect(cid)

                # Confirm deletion
                location_manager.delete_location(nearest_location["name"])
                print("Location deleted successfully!")
                root.destroy()
                display_map_with_menu(location_manager, route_history, graph)

        # Connect the event handler to the matplotlib figure
        cid = fig.canvas.mpl_connect('button_press_event', on_click)

    def search_location():
        location_name = simpledialog.askstring("Input", "Enter location name to search:", parent=root)
        result = location_manager.search_location(location_name)
        if result:
            print(f"Location found: {result}")
        else:
            print("Location not found.")

    def find_shortest_route():
        """Allow the user to select start and end locations on the map to find the shortest route."""
        print("Click on the map to select the start and end locations.")

        # Variables to store the selected locations
        selected_locations = []

        def on_click(event):
            nearest_location = select_nearest_location(event, location_manager.locations)
            if nearest_location:
                selected_locations.append(nearest_location)
                print(f"Selected location: {nearest_location['name']}")

                # If two locations are selected, find the shortest route
                if len(selected_locations) == 2:
                    fig.canvas.mpl_disconnect(cid)
                    start_location = selected_locations[0]["id"]
                    end_location = selected_locations[1]["id"]
                    route, totalDistance = graph.find_shortest_path(start_location, end_location)
                    if route:
                        locationNames = [location_manager.get_location_name(id) for id in route]
                        print(f"Shortest Route: {locationNames}\nDistance: {totalDistance}")
                    else:
                        print("No route found between the locations.")

        # Connect the event handler to the matplotlib figure
        cid = fig.canvas.mpl_connect('button_press_event', on_click)

    def view_route_history():
        history = route_history.get_history()
        print("Route History:")
        for route in history:
            print(route)

    menu_buttons = [
        ("Add a new location", add_location),
        ("Edit an existing location", edit_location),
        ("Delete a location", delete_location),
        ("Search for a location", search_location),
        ("Find shortest route", find_shortest_route),
        ("View route history", view_route_history),
        ("Exit", exit_application),
    ]

    for text, command in menu_buttons:
        button = tk.Button(menu_frame, text=text, command=command)
        button.pack(side=tk.LEFT, padx=5, pady=5)

    root.mainloop()


def main():
    location_manager = LocationManager()
    route_history = RouteHistory()
    graph = Graph()

    graphBuilder(graph, location_manager.get_location_ids())
    print(graph)

    display_map_with_menu(location_manager, route_history, graph)

if __name__ == "__main__":
    main()