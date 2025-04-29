# Standard Library Imports
import os

# Third-Party Imports
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import FancyBboxPatch
import matplotlib.pyplot as plt

# Local Imports
from location_manager import LocationManager
from route_history import RouteHistory
from data_structures.graph import Graph
from utils import extract_coordinates_and_labels, add_background_image, select_nearest_location

current_marker = None
normal_click_handler = None

def display_map_with_menu(location_manager, route_history, graph):
    """Display the map and menu options in a single GUI window."""
    global current_marker, normal_click_handler

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
        global current_marker

        # Remove the previous marker if it exists
        if current_marker and current_marker[0] in ax.lines:
            current_marker[0].remove()

        # Get the list of location names
        location_names = [location["name"] for location in location_manager.locations]

        if not location_names:
            print("No locations available to search.")
            return

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
            global current_marker

            selected_name = combo_box.get()
            if selected_name:
                result = location_manager.search_location(selected_name)
                if result:
                    x, y = result['x'], result['y']
                    print(f"Location found: {result['name']} at coordinates {x}, {y}")
                    
                    # Clear any previous marker and info card
                    clear_info_card()

                    # Add a static red dot at the selected location
                    current_marker = ax.plot(x, y, 'ro', markersize=12)

                    # Display the info card
                    text = result['name'] + '\n'
                    if result['name'] in location_manager.location_features:
                        text += '\nContains:'
                        for feature in location_manager.location_features[result['name']]:
                            text += '\n-' + feature
                    else:
                        text += '\nContains no notable\nfeatures or buildings.'

                    render_location_info(text)

                    # Redraw the canvas
                    canvas.draw()
                else:
                    print("Location not found.")
            popup.destroy()

        # Add a button to confirm selection
        confirm_button = tk.Button(popup, text="Search", command=on_select)
        confirm_button.pack(pady=10)

    textX, textY = 350, -70

    def clear_info_card():
        """Clear the currently displayed info card."""
        if hasattr(render_location_info, "previous_text_obj") and render_location_info.previous_text_obj:
            if render_location_info.previous_text_obj in ax.texts:
                render_location_info.previous_text_obj.remove()
            render_location_info.previous_text_obj = None

        if hasattr(render_location_info, "previous_box") and render_location_info.previous_box:
            if render_location_info.previous_box in ax.patches:
                render_location_info.previous_box.remove()
            render_location_info.previous_box = None

        canvas.draw()

    def render_location_info(text: str):
        clear_info_card()

        # Render the new text
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

        # Save references to the current text and box
        render_location_info.previous_text_obj = text_obj
        render_location_info.previous_box = box

        # Render to canvas
        canvas.draw()


    def normal_click(event):
        """Handle normal click events on the map."""
        global current_marker

        # Remove the previous marker if it exists
        if current_marker and current_marker[0] in ax.lines:
            current_marker[0].remove()
        
        clear_info_card()

        nearest_location = select_nearest_location(event, location_manager.get_visible_Locations())
    
        if nearest_location is None:
            return

        x, y = nearest_location['x'], nearest_location['y']
        
        # Add a static red dot at the selected location
        current_marker = ax.plot(x, y, 'ro', markersize=12)

        # Display the info card
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
        global current_marker, normal_click_handler

        # Remove the previous marker if it exists
        if current_marker and current_marker[0] in ax.lines:
            current_marker[0].remove()

        clear_info_card()

        fig.canvas.mpl_disconnect(normal_click_handler)

        print("Click on the map to select the start and end locations.")

        # Variables to store the selected locations
        selected_locations = []

        def on_click(event):
            global normal_click_handler

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
                        route_text = f"Shortest Route: {locationNames} (Distance: {totalDistance}m)"
                        print(route_text)

                        # Add the route to the history
                        route_history.add_route(route_text)
                       
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
                    
                    # Reconnect the normal click handler
                    normal_click_handler = fig.canvas.mpl_connect('button_press_event', normal_click)

        # Connect the event handler for selecting locations
        cid = fig.canvas.mpl_connect('button_press_event', on_click)

    def view_route_history():
        global current_marker

        # Remove the previous marker if it exists
        if current_marker and current_marker[0] in ax.lines:
            current_marker[0].remove()
            
        """Display route history with forward and back navigation."""
        clear_info_card()
        history = route_history.get_history()

        if not history:
            print("No route history available.")
            return

        # Create a popup window
        popup = tk.Toplevel(root)
        popup.title("Route History")
        popup.geometry("400x300")

        # Variables to track the current route index
        current_index = tk.IntVar(value=len(history) - 1)

        # Label to display the current route
        route_label = tk.Label(popup, text="", wraplength=350, justify="left")
        route_label.pack(pady=20)

        def update_route_label_and_map():
            """Update the label to show the current route."""
            
            # Get the current route from history
            route_text = history[current_index.get()]

            route_details = route_text.split(":")[1].strip()
            location_names_part = route_details.split(" (")[0]
            location_names = location_names_part.strip("[]").replace("'", "").split(", ")

            distance_start = route_text.rfind("(Distance: ") + len("(Distance: ")
            distance_end = route_text.rfind("m)")
            distance = route_text[distance_start:distance_end].strip()

            # Format the label to show only "from", "to", and "distance"
            if len(location_names) >= 2:
                from_location = location_names[0]
                to_location = location_names[-1]
                route_index = f"Route {current_index.get() + 1}/{len(history)}"
                route_label.config(
                    text=f"{route_index}\nFrom: {from_location}\nTo: {to_location}\nDistance: {distance}m",
                    font=("Arial", 18)
                )
            else:
                route_label.config(text="Invalid route data.")

            # Convert location names to IDs
            location_ids = [location_manager.get_location_id(name) for name in location_names]
            
            # Clear the previous route line from the map
            for line in ax.lines:
                if line.get_label() == "Shortest Route":
                    line.remove()

            # Get coordinates for the route and draw it on the map
            route_coords = [
                location_manager.get_location_coordinates(location_id) for location_id in location_ids
            ]
            x_coords, y_coords = zip(*route_coords)
            ax.plot(x_coords, y_coords, color="red", linewidth=2, label="Shortest Route")
            ax.legend()
            canvas.draw()

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

    for id in location_manager.get_location_ids():
        graph.add_node(id)

    graph.load_from_json("data/campus_map.json")

    display_map_with_menu(location_manager, route_history, graph)

if __name__ == "__main__":
    main()