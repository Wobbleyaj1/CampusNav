# Standard Library Imports
import os

# Third-Party Imports
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# Local Imports
from location_manager import LocationManager
from data_structures.stack import Stack
from data_structures.graph import Graph
from data_structures.queue import Queue
from data_structures.tree import Tree
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
        self.route_history = Stack()
        self.graph = Graph()
        self.location_tree = Tree()        

        for id in self.location_manager.get_location_ids():
            self.graph.add_node(id)

        self.graph.load_from_json("data/campus_map.json")

        self._initialize_location_tree()

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
            ("View location tree", self.build_location_tree),
            ("Exit", self.exit_application),
        ]
        self.buttons = add_menu_buttons(self.menu_frame, menu_buttons)

        self.root.protocol("WM_DELETE_WINDOW", self.exit_application)

        self.prompt_text_obj = None
        self.update_prompt_text()

    def disable_buttons(self):
        for button in self.buttons:
            button.config(state='disabled')

    def enable_buttons(self):
        for button in self.buttons:
            button.config(state='normal')

    def update_prompt_text(self, text: str = 'Click a location for more info'):
        x, y = -1260, -790
        if self.prompt_text_obj is not None:
            self.prompt_text_obj.remove()
            self.prompt_text_box.remove()

        self.prompt_text_obj = text_obj = self.ax.text(x, y, text, fontsize=12, va='bottom', ha='left', zorder=2)

        # Get bounding box of the text in data coordinates
        renderer = self.canvas.get_renderer()
        bbox = text_obj.get_window_extent(renderer=renderer)
        inv = self.ax.transData.inverted()
        bbox_data = bbox.transformed(inv)

        # Draw a box around the text
        width = bbox_data.width
        height = bbox_data.height
        self.prompt_text_box = FancyBboxPatch((x-5, y-5), width+15, height+15,
                            boxstyle="round,pad=0.3", edgecolor='black',
                            facecolor='lightyellow', zorder=1)
        self.ax.add_patch(self.prompt_text_box)

        # Redraw text on top
        self.ax.draw_artist(text_obj)

        # Render to canvas
        self.canvas.draw()

    def initialize_map(self):
        """Initialize the map with locations and background."""
        x_coords, y_coords, labels = extract_coordinates_and_labels(
            self.location_manager.get_visible_Locations()
        )
        add_background_image(self.ax, "./assets/mercer_map.png")
        self.ax.scatter(x_coords, y_coords, color="blue", label="Locations")
        self.ax.set_xticks([])
        self.ax.set_yticks([])
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
        self.update_prompt_text()

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

        # Clear any existing shortest route lines
        for line in self.ax.lines:
            line.remove()

        self.clear_info_card()

        # Check if a popup is already open
        if hasattr(self, "current_popup") and self.current_popup is not None and self.current_popup.winfo_exists():
            self.current_popup.lift()  # Bring the existing popup to the front
            return

        # Create a new popup
        self.current_popup = create_popup_window("Search Location", 300, 150)

        label = tk.Label(self.current_popup, text="Select a location:")
        label.pack(pady=10)

        location_names = [location["name"] for location in self.location_manager.locations]

        if not location_names:
            self.current_popup.destroy()
            return

        combo_box = ttk.Combobox(self.current_popup, values=location_names, state="readonly")
        combo_box.pack(pady=10)
        combo_box.set("Select a location")

        def on_select():
            selected_name = combo_box.get()
            if selected_name:
                result = self.location_manager.search_location(selected_name)
                if result:
                    x, y = result['x'], result['y']
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
                    return
            self.current_popup.destroy()

        confirm_button = tk.Button(self.current_popup, text="Search", command=on_select)
        confirm_button.pack(pady=10)

    def find_shortest_route(self):
        self.disable_buttons()
        self.update_prompt_text('Select Starting Point')

        """Allow the user to select start and end locations on the map to find the shortest route."""
        # Clear the current marker if it exists
        clear_current_marker(self.current_marker, self.ax)

        self.clear_info_card()

        # Disconnect the normal click handler
        self.fig.canvas.mpl_disconnect(self.normal_click_handler)

        # Variables to store the selected locations
        selected_locations = []

        def on_click(event):
            nearest_location = select_nearest_location(event, self.location_manager.get_visible_Locations())
            if nearest_location:
                selected_locations.append(nearest_location)

                # If two locations are selected, find the shortest route
                if len(selected_locations) == 2:
                    self.fig.canvas.mpl_disconnect(cid)  # Disconnect the shortest route click handler
                    start_location = selected_locations[0]["id"]
                    end_location = selected_locations[1]["id"]
                    route, total_distance = self.graph.find_shortest_path(start_location, end_location)
                    if route:
                        location_names = [self.location_manager.get_location_name(location_id) for location_id in route]
                        route_text = f"Shortest Route: {location_names} (Distance: {total_distance}m)"

                        # Add the route to the history directly using Stack
                        self.route_history.push(route_text)

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

                        self.update_prompt_text()
                        self.enable_buttons()

                    # Reconnect the normal click handler
                    self.normal_click_handler = self.fig.canvas.mpl_connect('button_press_event', self.normal_click)

                elif len(selected_locations) == 1:
                    self.update_prompt_text('Select End Location')
        # Connect the event handler for selecting locations
        cid = self.fig.canvas.mpl_connect('button_press_event', on_click)

    def view_route_history(self):
        """Display route history with forward and back navigation."""
        # Clear the current marker if it exists
        clear_current_marker(self.current_marker, self.ax)

        self.clear_info_card()

        # Check if a popup is already open
        if hasattr(self, "current_popup") and self.current_popup is not None and self.current_popup.winfo_exists():
            self.current_popup.lift()
            self.current_popup.destroy()
            return

        # Create a new popup
        self.current_popup = create_popup_window("Route History", 400, 300)

        history = self.route_history.list

        if not history:
            self.current_popup.destroy()
            self.update_prompt_text('No Route History Available')
            return

        current_index = tk.IntVar(value=len(history) - 1)

        route_label = tk.Label(self.current_popup, text="", wraplength=350, justify="left")
        route_label.pack(pady=20)

        def update_route_label_and_map():
            """Update the label to show the current route."""
            route_text = history[current_index.get()]
            location_names, distance = parse_route_details(route_text)
            route_label.config(
                text=format_route_label(current_index.get(), history, location_names, distance),
                font=("Arial", 18)
            )
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
        back_button = tk.Button(self.current_popup, text="Back", command=go_back)
        back_button.pack(side=tk.LEFT, padx=10, pady=10)

        forward_button = tk.Button(self.current_popup, text="Forward", command=go_forward)
        forward_button.pack(side=tk.RIGHT, padx=10, pady=10)

        update_route_label_and_map()

    def walking_guide(self):
        self.update_prompt_text('Select Starting Location')
        self.disable_buttons()

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

                    self.update_prompt_text()
                    self.enable_buttons()
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
                        self.route_history.push(route_text)

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

                        self.update_prompt_text('Click to Move to Next Location')

                    else:
                        self.update_prompt_text('Selected Locations are Not Connected')
                        print("No route found between the selected locations.")
                        # Reconnect the normal click handler
                        self.normal_click_handler = self.fig.canvas.mpl_connect('button_press_event', self.normal_click)

                elif len(selected_locations) == 1:
                    self.update_prompt_text('Select End Location')

        # Connect the event handler for selecting locations
        cid = self.fig.canvas.mpl_connect('button_press_event', on_click)

    def _initialize_location_tree(self):
        """Initialize the tree structure for campus locations."""
        root = "Campus"
        self.location_tree.add_node(root)

        # Group locations by their categories from the JSON file
        categories = {}
        for location in self.location_manager.locations:
            category = location.get("category", "Miscellaneous")
            location_name = location["name"]

            if category not in categories:
                categories[category] = []
                self.location_tree.add_node(category)
                self.location_tree.nodes[root].append(category)

            categories[category].append(location_name)
            self.location_tree.add_node(location_name)
            self.location_tree.nodes[category].append(location_name)

    def build_location_tree(self):
        """Build and display the tree structure for campus locations in a popup."""
        # Check if a popup is already open
        if hasattr(self, "current_popup") and self.current_popup is not None and self.current_popup.winfo_exists():
            self.current_popup.lift()  # Bring the existing popup to the front
            self.current_popup.destroy()
            return

        # Create a popup window to display the tree
        self.current_popup = create_popup_window("Location Tree", 400, 300)

        tree_view = ttk.Treeview(self.current_popup)
        tree_view.pack(fill=tk.BOTH, expand=True)

        # Add nodes to the Treeview widget
        def add_tree_nodes(parent, node):
            for child in self.location_tree.get_children(node):
                tree_view.insert(parent, "end", child, text=child)
                add_tree_nodes(child, child)

        # Add the root node and recursively add its children
        root = "Campus"
        tree_view.insert("", "end", root, text=root)
        add_tree_nodes(root, root)

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