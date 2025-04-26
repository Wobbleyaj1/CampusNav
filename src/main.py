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
from utils import extract_coordinates_and_labels, add_background_image, get_location_details, refresh_map

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
        location_name = simpledialog.askstring("Input", "Enter location name to edit:", parent=root)
        new_coordinates = simpledialog.askstring("Input", "Enter new coordinates (x,y):", parent=root)
        location_manager.edit_location(location_name, new_coordinates)
        print("Location updated successfully!")
        root.destroy()
        display_map_with_menu(location_manager, route_history, graph)

    def delete_location():
        location_name = simpledialog.askstring("Input", "Enter location name to delete:", parent=root)
        location_manager.delete_location(location_name)
        print("Location deleted successfully!")
        root.destroy()
        display_map_with_menu(location_manager, route_history, graph)

    def search_location():
        location_name = simpledialog.askstring("Input", "Enter location name to search:", parent=root)
        result = location_manager.search_location(location_name)
        if result:
            print(f"Location found: {result}")
        else:
            print("Location not found.")

    def find_shortest_route():
        dialog = tk.Toplevel(root)
        dialog.title('Find Shortest Route')

        frame = ttk.Frame(dialog)
        frame.pack(padx=10, pady=10)

        ttk.Label(frame, text='Current Location:').grid(row=0, column=0, padx=5, pady=5)

        comboCurr = ttk.Combobox(frame, values=location_manager.get_location_names())
        comboCurr.grid(row=1, column=0, padx=5, pady=5)
        comboCurr.current(0)

        ttk.Label(frame, text='Destination:').grid(row=0, column=1, padx=5, pady=5)

        comboDest = ttk.Combobox(frame, values=location_manager.get_location_names())
        comboDest.grid(row=1, column=1, padx=5, pady=5)
        comboDest.current(0)

        def submit():
            currName = comboCurr.get()
            destName = comboDest.get()
            print(currName, destName)
            dialog.destroy()

            if currName == destName:
                return

            currId = location_manager.get_location_id(currName)
            destId = location_manager.get_location_id(destName)

            path, totalDistance = graph.find_shortest_path(currId, destId)
            namedPath = []
            for id in path:
                namedPath.append(location_manager.get_location_name(id))
            print(namedPath, totalDistance)

            resultDialog = tk.Toplevel(root)
            resultDialog.title('Find Shortest Route')
            resultFrame = ttk.Frame(resultDialog)
            resultFrame.pack(padx=10, pady=10)
            for i in range(len(namedPath) - 1):
                ttk.Label(resultFrame, text=f'{namedPath[i]} -> {namedPath[i+1]}').grid(row=i, column=0, padx=5, pady=5)
            ttk.Label(resultFrame, text=f'Total Distance: {totalDistance}m').grid(row=i+1, column=0, padx=5, pady=5)

            route_history.add_route((namedPath, totalDistance))

        ttk.Button(dialog, text='OK', command=submit).pack(pady=5)


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