# Standard Library Imports
import os

# Third-Party Imports
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Local Imports
from location_manager import LocationManager
from route_history import RouteHistory
from data_structures.graph import Graph
from data_structures.queue import Queue
from utils import (
    extract_coordinates_and_labels,
    add_background_image,
    select_nearest_location,
    parse_route_details,
    format_route_label,
    update_route_on_map,
    create_popup_window,
    clear_current_marker,
    render_location_info,
    add_menu_buttons,
)

class CampusNavigationApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Campus Navigation System")
        self.root.geometry("1000x800")

        self.current_marker = None

        self.location_manager = LocationManager()
        self.route_history = RouteHistory()
        self.graph = Graph()

        for id in self.location_manager.get_location_ids():
            self.graph.add_node(id)

        self.graph.load_from_json("data/campus_map.json")

        # Create the map and menu frames
        self.map_frame = tk.Frame(self.root)
        self.map_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Initialize the map
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.map_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

        self.initialize_map()

        # Connect the normal click handler after initializing the map
        self.normal_click_handler = self.fig.canvas.mpl_connect('button_press_event', self.normal_click)

        # Add menu buttons
        menu_buttons = [
            ("Search for a location", self.search_location),
            ("Find shortest route", self.find_shortest_route),
            ("View route history", self.view_route_history),
            ("Walking Guide", self.walking_guide),
            ("Exit", self.exit_application),
        ]
        add_menu_buttons(self.menu_frame, menu_buttons)

        self.root.protocol("WM_DELETE_WINDOW", self.exit_application)

    def initialize_map(self):
        """Initialize the map with locations and background."""
        x_coords, y_coords, labels = extract_coordinates_and_labels(
            self.location_manager.get_visible_Locations()
        )
        add_background_image(self.ax, "./assets/mercer_map.png")
        self.ax.scatter(x_coords, y_coords, color="blue", label="Locations")
        self.ax.set_xlabel("X Coordinate")
        self.ax.set_ylabel("Y Coordinate")
        self.ax.set_title("Campus Map")
        self.ax.set_aspect(aspect=1006 / 978)
        self.ax.legend()

    def clear_info_card(self):
        """Clear the currently displayed info card."""
        if hasattr(render_location_info, "previous_text_obj") and render_location_info.previous_text_obj:
            if render_location_info.previous_text_obj in self.ax.texts:
                render_location_info.previous_text_obj.remove()
            render_location_info.previous_text_obj = None

        if hasattr(render_location_info, "previous_box") and render_location_info.previous_box:
            if render_location_info.previous_box in self.ax.patches:
                render_location_info.previous_box.remove()
            render_location_info.previous_box = None

        self.canvas.draw()

    def display_info_card(self, name: str, x: int = 350, y: int = -120):
        # Display the info card
        text = name + '\n'

        if name in self.location_manager.location_features:
            text += '\nContains:'
            for feature in self.location_manager.location_features[name]:
                text += '\n- ' + feature
        else:
            text += '\nContains no notable\nfeatures or buildings.'

        # Offset the info card position slightly to avoid overlap with the dot
        render_location_info(self.ax, self.canvas, text, x + 100, y)

    def normal_click(self, event):
        """Handle normal click events on the map."""
        clear_current_marker(self.current_marker, self.ax)

        self.clear_info_card()

        nearest_location = select_nearest_location(event, self.location_manager.get_visible_Locations())

        if nearest_location is None:
            return

        x, y = nearest_location['x'], nearest_location['y']

        # Add a static red dot at the selected location
        self.current_marker = self.ax.plot(x, y, 'ro', markersize=12)

        # Display the info card
        self.display_info_card(nearest_location['name'], x, y)

    def search_location(self):
        """Allow the user to search for a location using a combo box and display its information."""
        clear_current_marker(self.current_marker, self.ax)

        location_names = [location["name"] for location in self.location_manager.locations]

        if not location_names:
            print("No locations available to search.")
            return

        popup = create_popup_window("Search Location", 300, 150)

        label = tk.Label(popup, text="Select a location:")
        label.pack(pady=10)

        combo_box = ttk.Combobox(popup, values=location_names, state="readonly")
        combo_box.pack(pady=10)
        combo_box.set("Select a location")

        def on_select():
            selected_name = combo_box.get()
            if selected_name:
                result = self.location_manager.search_location(selected_name)
                if result:
                    x, y = result['x'], result['y']
                    print(f"Location found: {result['name']} at coordinates {x}, {y}")
                    self.clear_info_card()
                    self.current_marker = self.ax.plot(x, y, 'ro', markersize=12)

                    text = result['name'] + '\n'
                    if result['name'] in self.location_manager.location_features:
                        text += '\nContains:'
                        for feature in self.location_manager.location_features[result['name']]:
                            text += '\n- ' + feature
                    else:
                        text += '\nContains no notable\nfeatures or buildings.'

                    # Offset the info card position slightly to avoid overlap with the dot
                    render_location_info(self.ax, self.canvas, text, x + 100, y)
                    self.canvas.draw()
                else:
                    print("Location not found.")
            popup.destroy()

        confirm_button = tk.Button(popup, text="Search", command=on_select)
        confirm_button.pack(pady=10)

    def find_shortest_route(self):
        """Allow the user to select start and end locations on the map to find the shortest route."""
        # Clear the current marker if it exists
        clear_current_marker(self.current_marker, self.ax)

        self.clear_info_card()

        print("Click on the map to select the start and end locations.")

        # Disconnect the normal click handler
        self.fig.canvas.mpl_disconnect(self.normal_click_handler)

        # Variables to store the selected locations
        selected_locations = []

        def on_click(event):
            nearest_location = select_nearest_location(event, self.location_manager.get_visible_Locations())
            if nearest_location:
                selected_locations.append(nearest_location)
                print(f"Selected location: {nearest_location['name']}")

                # If two locations are selected, find the shortest route
                if len(selected_locations) == 2:
                    self.fig.canvas.mpl_disconnect(cid)  # Disconnect the shortest route click handler
                    start_location = selected_locations[0]["id"]
                    end_location = selected_locations[1]["id"]
                    route, total_distance = self.graph.find_shortest_path(start_location, end_location)
                    if route:
                        location_names = [self.location_manager.get_location_name(location_id) for location_id in route]
                        route_text = f"Shortest Route: {location_names} (Distance: {total_distance}m)"
                        print(route_text)

                        # Add the route to the history
                        self.route_history.add_route(route_text)

                        # Clear the previous route
                        for line in self.ax.lines:
                            line.remove()

                        # Extract coordinates for the route
                        route_coords = [
                            self.location_manager.get_location_coordinates(location_id) for location_id in route
                        ]
                        x_coords, y_coords = zip(*route_coords)

                        # Draw the route on the map
                        self.ax.plot(x_coords, y_coords, color="red", linewidth=2, label="Shortest Route")
                        self.ax.legend()
                        self.canvas.draw()
                    else:
                        print("No route found between the selected locations.")

                    # Reconnect the normal click handler
                    self.normal_click_handler = self.fig.canvas.mpl_connect('button_press_event', self.normal_click)

        # Connect the event handler for selecting locations
        cid = self.fig.canvas.mpl_connect('button_press_event', on_click)

    def view_route_history(self):
        """Display route history with forward and back navigation."""
        # Clear the current marker if it exists
        if self.current_marker and self.current_marker[0] in self.ax.lines:
            self.current_marker[0].remove()

        self.clear_info_card()

        history = self.route_history.get_history()

        if not history:
            print("No route history available.")
            return

        # Create a popup window
        popup = create_popup_window("Route History", 400, 300)

        # Variables to track the current route index
        current_index = tk.IntVar(value=len(history) - 1)

        # Label to display the current route
        route_label = tk.Label(popup, text="", wraplength=350, justify="left")
        route_label.pack(pady=20)

        def update_route_label_and_map():
            """Update the label to show the current route."""
            # Get the current route from history
            route_text = history[current_index.get()]
            location_names, distance = parse_route_details(route_text)

            # Format the label to show only "from", "to", and "distance"
            route_label.config(
                text=format_route_label(current_index.get(), history, location_names, distance),
                font=("Arial", 18)
            )

            # Update the route on the map
            update_route_on_map(self.ax, self.canvas, self.location_manager, location_names)

        def go_back():
            """Go to the previous route."""
            if current_index.get() > 0:
                current_index.set(current_index.get() - 1)
                update_route_label_and_map()

        def go_forward():
            """Go to the next route."""
            if current_index.get() < len(history) - 1:
                current_index.set(current_index.get() + 1)
                update_route_label_and_map()

        # Navigation buttons
        back_button = tk.Button(popup, text="Back", command=go_back)
        back_button.pack(side=tk.LEFT, padx=10, pady=10)

        forward_button = tk.Button(popup, text="Forward", command=go_forward)
        forward_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # Initialize the label with the first route
        update_route_label_and_map()

    def walking_guide(self):
        # Clear the current marker if it exists
        clear_current_marker(self.current_marker, self.ax)

        self.clear_info_card()

        print("Click on the map to select the start and end locations.")

        # Disconnect the normal click handler
        self.fig.canvas.mpl_disconnect(self.normal_click_handler)

        # Variables to store the selected locations
        selected_locations = []

        # Keeps track of if the user has set a path
        self.route_set = False
        self.walking_queue = Queue()
        self.walking_x = None
        self.walking_y = None

        def on_click(event):
            "Adds a walking guide that helps a used navigate to a location"
            nearest_location = select_nearest_location(event, self.location_manager.get_visible_Locations())

            if self.route_set:
                if len(self.walking_queue) == 0:
                    # Disconnect the shortest route click handler
                    self.fig.canvas.mpl_disconnect(cid)

                    # Clear the route
                    self.clear_info_card()

                    for line in self.ax.lines:
                        line.remove()

                    clear_current_marker(self.current_marker, self.ax)
                    self.ax.legend()
                    self.canvas.draw()

                    # Reconnect the normal click handler
                    self.normal_click_handler = self.fig.canvas.mpl_connect('button_press_event', self.normal_click)

                    return
                
                clear_current_marker(self.current_marker, self.ax)
                self.clear_info_card()

                prev_x = self.walking_x
                prev_y = self.walking_y
                self.walking_x, self.walking_y = self.walking_queue.dequeue()

                # Add a static red dot at the selected location
                self.current_marker = self.ax.plot(self.walking_x, self.walking_y, 'co', markersize=6, label='Last Location')

                # Add new finish path
                self.ax.plot([prev_x, self.walking_x], [prev_y, self.walking_y], color="cyan", linewidth=2)
                self.canvas.draw()

                # Display Info for Points of Interest
                name = self.location_manager.get_location_name_from_cords(self.walking_x, self.walking_y)
                if self.location_manager.is_point_of_interest(name):
                    self.display_info_card(name)

                print(f'Moved to: {name} ({self.walking_x}, {self.walking_y})')

            elif nearest_location:
                selected_locations.append(nearest_location)
                print(f"Selected location: {nearest_location['name']}")

                # If two locations are selected, find the shortest route
                if len(selected_locations) == 2:
                    start_location = selected_locations[0]["id"]
                    end_location = selected_locations[1]["id"]
                    route, total_distance = self.graph.find_shortest_path(start_location, end_location)
                    if route:
                        location_names = [self.location_manager.get_location_name(location_id) for location_id in route]
                        route_text = f"Shortest Route: {location_names} (Distance: {total_distance}m)"
                        print(route_text)

                        # Add the route to the history
                        self.route_history.add_route(route_text)

                        # Clear the previous route
                        for line in self.ax.lines:
                            line.remove()

                        # Extract coordinates for the route
                        route_coords = [
                            self.location_manager.get_location_coordinates(location_id) for location_id in route
                        ]
                        x_coords, y_coords = zip(*route_coords)

                        self.walking_queue = Queue(route_coords)
                        self.walking_x, self.walking_y = self.walking_queue.dequeue()

                        # Draw the route on the map
                        self.ax.plot(x_coords, y_coords, color="white", linewidth=2, label="Planed Route")
                        self.ax.plot(self.walking_x, self.walking_y, color="cyan", linewidth=2, label="Past Route")
                        self.current_marker = self.ax.plot(self.walking_x, self.walking_y, 'co', markersize=6, label='Current Location')
                        self.ax.legend()
                        self.canvas.draw()

                        # Display Info for Points of Interest
                        name = self.location_manager.get_location_name_from_cords(self.walking_x, self.walking_y)
                        if self.location_manager.is_point_of_interest(name):
                            self.display_info_card(name)
                        
                        self.route_set = True
                    else:
                        print("No route found between the selected locations.")
                        # Reconnect the normal click handler
                        self.normal_click_handler = self.fig.canvas.mpl_connect('button_press_event', self.normal_click)

        # Connect the event handler for selecting locations
        cid = self.fig.canvas.mpl_connect('button_press_event', on_click)

    def exit_application(self):
        """Exit the application cleanly."""
        print("Thank you for using Campus Navigation System!")
        self.root.destroy()
        os._exit(0)

    def run(self):
        """Run the main application loop."""
        self.root.mainloop()


if __name__ == "__main__":
    app = CampusNavigationApp()
    app.run()