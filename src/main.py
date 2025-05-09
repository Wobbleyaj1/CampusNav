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
from data_structures.array import Array, LinkedStructures
from data_structures.set import Set
from data_structures.list import List
from data_structures.searching_sorting import Searching, Sorting
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
        self.frequent_locations = Array(size=10, default_value=None)
        self.current_route = LinkedStructures()
        self.recent_locations = List()
        self.searching = Searching()
        self.sorting = Sorting()

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
            ("Walking Guide", self.walking_guide),
            ("View route history", self.view_route_history),
            ("View location tree", self.build_location_tree),
            ("Searched Locations", self.display_frequent_locations),
            ("Clicked Locations", self.display_recent_locations),
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
        """Display the info card with constraints to keep it within the map bounds."""
        # Display the info card text
        text = name + '\n'

        if name in self.location_manager.location_features:
            text += '\nContains:'
            for feature in self.location_manager.location_features[name]:
                text += '\n- ' + feature
        else:
            text += '\nContains no notable\nfeatures or buildings.'

        # Get the map's visible bounds
        x_min, x_max = self.ax.get_xlim()
        y_min, y_max = self.ax.get_ylim()

        # Constrain the info card position to stay within the map bounds
        constrained_x = max(x_min + 50, min(x + 100, x_max - 200))  # Add padding to avoid edges
        constrained_y = max(y_min + 50, min(y, y_max - 100))        # Add padding to avoid edges

        # Render the info card at the constrained position
        render_location_info(self.ax, self.canvas, text, constrained_x, constrained_y)

    def normal_click(self, event):
        self.update_prompt_text()

        """Handle normal click events on the map."""
        clear_current_marker(self.current_marker, self.ax)

        self.clear_info_card()

        nearest_location = select_nearest_location(event, self.location_manager.get_visible_Locations())

        if nearest_location is None:
            return
        
        self.access_location(nearest_location['name'])

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

        popup = self.manage_popup("Search Location", 300, 150)

        label = tk.Label(popup, text="Select a location:")
        label.pack(pady=10)

        location_names = [location["name"] for location in self.location_manager.locations]

        if not location_names:
            popup.destroy()
            return
        
        # Sort the location names alphabetically
        sorted_location_names = self.sorting.merge_sort(location_names)


        combo_box = ttk.Combobox(popup, values=sorted_location_names, state="readonly")
        combo_box.pack(pady=10)
        combo_box.set("Select a location")

        def on_select():
            selected_name = combo_box.get()
            if selected_name:
                # Use binary search to find the location
                index = self.searching.binary_search(sorted_location_names, selected_name)
                if index != -1:
                    result = self.location_manager.search_location(selected_name)
                    if result:
                        # Store the location in the frequent_locations array
                        for i in range(self.frequent_locations.size):
                            if self.frequent_locations.get(i) is None:
                                self.frequent_locations.set(i, selected_name)
                                break
                            elif self.frequent_locations.get(i) == selected_name:
                                # Avoid duplicates
                                break
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
                    tk.messagebox.showerror("Error", "Location not found!")
                    return
            self.current_popup.destroy()

        confirm_button = tk.Button(popup, text="Search", command=on_select)
        confirm_button.pack(pady=10)

    def find_shortest_route(self):
        """Allow the user to select start and end locations on the map to find the shortest route."""
        self.disable_buttons()
        self.update_prompt_text('Select Starting Point')

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
                        # Clear the current route before adding the new one
                        self.current_route = LinkedStructures()

                        # Store the route in the LinkedStructures instance
                        for location_id in route:
                            self.current_route.add_node(location_id)

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

                        self.update_prompt_text(f'Total Distance: {total_distance}m')
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

        popup = self.manage_popup("Route History", 400, 300)

        history = self.route_history.list

        if not history:
            popup.destroy()
            self.update_prompt_text('No Route History Available')
            return

        current_index = tk.IntVar(value=len(history) - 1)

        route_label = tk.Label(popup, text="", wraplength=350, justify="left")
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
        back_button = tk.Button(popup, text="Back", command=go_back)
        back_button.pack(side=tk.LEFT, padx=10, pady=10)

        forward_button = tk.Button(popup, text="Forward", command=go_forward)
        forward_button.pack(side=tk.RIGHT, padx=10, pady=10)

        update_route_label_and_map()

    def walking_guide(self):
        """Guide the user step-by-step through the current route."""
        if not self.current_route.head:
            self.update_prompt_text("No route available. Please find a route first.")
            return

        self.update_prompt_text("Starting walking guide...")
        self.disable_buttons()

        # Initialize a queue to store the locations in the route
        location_queue = Queue()

        # Initialize the current node for traversal
        current_node = self.current_route.head
        while current_node:
            location_queue.enqueue(current_node.value)
            current_node = current_node.next

        def move_to_next_location():
            """Move to the next location in the route."""
            if location_queue.isEmpty():
                self.update_prompt_text("Walking guide completed!")
                self.enable_buttons()
                next_button.destroy()  # Remove the button when the guide is complete
                return

            location_id = location_queue.dequeue()
            x, y = self.location_manager.get_location_coordinates(location_id)

            # Highlight the current location on the map
            self.ax.plot(x, y, 'wo', markersize=10, label="Current Location")
            self.canvas.draw()

            # Display information about the current location
            name = self.location_manager.get_location_name(location_id)
            if self.location_manager.is_point_of_interest(name):
                self.display_info_card(name)

            # Update the prompt text
            self.update_prompt_text(f"Currently at {name}. Click 'Next' to continue...")

        # Create a "Next" button for navigation
        next_button = tk.Button(self.root, text="Next", command=move_to_next_location)
        next_button.pack(pady=10)

        # Start the guide by moving to the first location
        move_to_next_location()

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
        popup = self.manage_popup("Location Tree", 400, 300)

        tree_view = ttk.Treeview(popup)
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

    def display_frequent_locations(self):
        """Display the list of frequently accessed locations."""
        popup = self.manage_popup("Frequent Locations", 300, 200)

        label = tk.Label(popup, text="Frequently Accessed Locations:")
        label.pack(pady=10)

        # Ensure only unique locations are stored in the array
        unique_locations = Set()
        for i in range(self.frequent_locations.size):
            location = self.frequent_locations.get(i)
            if location is not None:
                unique_locations.add(location)

        # Convert the set to a list and sort it alphabetically
        sorted_locations = self.sorting.merge_sort(list(unique_locations))

         # Display the sorted unique locations
        if sorted_locations:
            for location in sorted_locations:
                location_label = tk.Label(popup, text=location)
                location_label.pack()
        else:
            no_locations_label = tk.Label(popup, text="No locations accessed yet.")
            no_locations_label.pack()

    def access_location(self, location_name):
        """Access a location and add it to the recent locations list."""
        if not self.recent_locations.contains(location_name):
            self.recent_locations.add(location_name)

    def display_recent_locations(self):
        """Display the list of recently accessed locations."""
        popup = self.manage_popup("Recently Accessed Locations", 300, 200)

        label = tk.Label(popup, text="Recently Accessed Locations:")
        label.pack(pady=10)

        # Retrieve the recent locations as a list
        recent_locations = [self.recent_locations.get(i) for i in range(self.recent_locations.size())]

        # Sort the recent locations alphabetically
        sorted_recent_locations = self.sorting.quick_sort(recent_locations)

        # Display the sorted recent locations
        if sorted_recent_locations:
            for location in sorted_recent_locations:
                location_label = tk.Label(popup, text=location)
                location_label.pack()
        else:
            no_locations_label = tk.Label(popup, text="No locations accessed yet.")
            no_locations_label.pack()

    def manage_popup(self, title: str, width: int, height: int):
        """Manage popups to ensure only one is active at a time."""
        if hasattr(self, "current_popup") and self.current_popup is not None and self.current_popup.winfo_exists():
            self.current_popup.destroy()  # Destroy the existing popup

        # Create a new popup
        self.current_popup = create_popup_window(title, width, height)
        return self.current_popup
    
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