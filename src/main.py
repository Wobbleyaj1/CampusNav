# Standard Library Imports
import os

# Third-Party Imports
import tkinter as tk
from tkinter import simpledialog, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import FancyBboxPatch
import matplotlib.pyplot as plt

# Local Imports
from location_manager import LocationManager
from route_history import RouteHistory
from data_structures.graph import Graph
from graph_builder import graphBuilder
from utils import extract_coordinates_and_labels, add_background_image, get_location_details, refresh_map, select_nearest_location
from matplotlib.animation import FuncAnimation

def animate_marker(ax, canvas, x, y, interval=500):
    """Animate a blinking marker at the given coordinates."""
    marker, = ax.plot([], [], 'ro', markersize=12)

    def update(frame):
        # Alternate between visible and invisible
        if frame % 2 == 0:
            marker.set_data([x], [y]) 
        else:
            marker.set_data([], [])
        return marker,

    # Create the animation
    ani = FuncAnimation(
        ax.figure, update, frames=10, interval=interval, blit=True, repeat=False
    )

    # Redraw the canvas to show the animation
    canvas.draw()

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
    x_coords, y_coords, labels = extract_coordinates_and_labels(location_manager.get_visible_Locations())
    add_background_image(ax, "./assets/mercer_map.png")
    ax.scatter(x_coords, y_coords, color="blue", label="Locations")
    # for i, label in enumerate(labels):
    #     ax.annotate(label, (x_coords[i], y_coords[i]), textcoords="offset points", xytext=(5, 5), ha="center")
    ax.set_xlabel("X Coordinate")
    ax.set_ylabel("Y Coordinate")
    ax.set_title("Campus Map")
    ax.set_aspect(aspect = 1006 / 978)
    ax.legend()

    # Embed the matplotlib figure into the tkinter window
    canvas = FigureCanvasTkAgg(fig, master=map_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)

    def search_location():
        """Allow the user to search for a location using a combo box and display its coordinates."""
        # Get the list of location names
        location_names = [location["name"] for location in location_manager.locations]

        if not location_names:
            print("No locations available to search.")
            return

        # Create a popup window
        popup = tk.Toplevel(root)
        popup.title("Search Location")
        popup.geometry("300x150")

        # Add a label
        label = tk.Label(popup, text="Select a location:")
        label.pack(pady=10)

        # Add a combo box
        combo_box = ttk.Combobox(popup, values=location_names, state="readonly")
        combo_box.pack(pady=10)
        combo_box.set("Select a location")

        # Function to handle selection
        def on_select():
            selected_name = combo_box.get()
            if selected_name:
                result = location_manager.search_location(selected_name)
                if result:
                    x, y = result['x'], result['y']
                    print(f"Location found: {result['name']} at coordinates {x}, {y}")
                    animate_marker(ax, canvas, x, y)
                else:
                    print("Location not found.")
            popup.destroy()

        # Add a button to confirm selection
        confirm_button = tk.Button(popup, text="Search", command=on_select)
        confirm_button.pack(pady=10)

    textX, textY = 350, -70

    def render_location_info(text: str):
        text_obj = ax.text(textX, textY, text, va='top', ha='left')

        renderer = canvas.get_renderer()
        bbox = text_obj.get_window_extent(renderer=renderer)
        inv = ax.transData.inverted()
        bbox_data = bbox.transformed(inv)

        # Draw a box around the text
        width = bbox_data.width
        height = bbox_data.height
        box = FancyBboxPatch((textX - 10, textY - height - 10), width + 20, height + 20,
                            boxstyle="round,pad=3", edgecolor='black',
                            facecolor='lightyellow', zorder=1)
        ax.add_patch(box)

        # Redraw text on top
        ax.draw_artist(text_obj)

        # Render to canvas
        canvas.draw()

    def normal_click(event):
        nearest_location = select_nearest_location(event, location_manager.get_visible_Locations())
        x, y = nearest_location['x'], nearest_location['y']
        animate_marker(ax, canvas, x, y, 100)

        text = nearest_location['name'] + '\n'

        if nearest_location['name'] in location_manager.location_features:
            text += '\nContains:'

            for feature in location_manager.location_features[nearest_location['name']]:
                text += '\n-' + feature
        
        else:
            text += '\nContains no notable\nfeatures or buildings.'

        render_location_info(text)
        
    normal_click_handler = fig.canvas.mpl_connect('button_press_event', normal_click)

    def find_shortest_route():
        """Allow the user to select start and end locations on the map to find the shortest route."""
        fig.canvas.mpl_disconnect(normal_click_handler)

        print("Click on the map to select the start and end locations.")

        # Variables to store the selected locations
        selected_locations = []

        def on_click(event):
            nearest_location = select_nearest_location(event, location_manager.get_visible_Locations())
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
                        print(f"Shortest Route: {locationNames}{start_location} to {end_location}\nDistance: {totalDistance}")
                       
                        # Clear the previous route
                        for line in ax.lines:
                            line.remove()

                        # Extract coordinates for the route
                        route_coords = [
                            (location_manager.get_location_coordinates(id)) for id in route
                        ]
                        x_coords, y_coords = zip(*route_coords)

                        # Draw the route on the map
                        ax.plot(x_coords, y_coords, color="red", linewidth=2, label="Shortest Route")
                        ax.legend()
                        canvas.draw()
                    else:
                        print("No route found between the locations.")
                    fig.canvas.mpl_connect('button_press_event', normal_click)

        # Connect the event handler to the matplotlib figure
        cid = fig.canvas.mpl_connect('button_press_event', on_click)

    def view_route_history():
        history = route_history.get_history()
        print("Route History:")
        for route in history:
            print(route)

    menu_buttons = [
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

    display_map_with_menu(location_manager, route_history, graph)

if __name__ == "__main__":
    main()